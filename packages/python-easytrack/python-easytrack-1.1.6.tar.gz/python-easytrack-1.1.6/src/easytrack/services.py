'''Services module for making modifications to database.'''

from datetime import datetime
from typing import Dict, List, Optional, Union

# app
from . import selectors as slc
from . import models as mdl
from . import wrappers
from .utils import notnull


def create_user(email: str, name: str, session_key: str) -> mdl.User:
    """
    Creates a user object in database and returns User object
    :param email: email of the user
    :param name: name of the user
    :param session_key: session key of the user
    :return: User object
    """

    return mdl.User.create(
        email = notnull(email),
        name = notnull(name),
        session_key = notnull(session_key),
    )


def set_user_session_key(user: mdl.User, new_session_key: str):
    """
    Sets a new session key for a user
    :param user: user object to be modified
    :param new_session_key: new session key
    :return: None
    """

    user.session_key = notnull(new_session_key)
    user.save()


def add_campaign_participant(campaign: mdl.Campaign, add_user: mdl.User) -> bool:
    """
    Binds user with campaign, making a participant.
    :param add_user: User object to be bound to a campaign
    :param campaign: Campaign object that user binds with
    :return: whether user has been bound (false if already bound)
    """

    if slc.is_participant(user = notnull(add_user), campaign = notnull(campaign)):
        return False

    # 1. bind the user to campaign
    participant = mdl.Participant.create(campaign = campaign, user = add_user)

    # 2. create a new data table for the participant
    for data_source in slc.get_campaign_data_sources(campaign = campaign):
        wrappers.DataTable(participant = participant, data_source = data_source).create_table()
        wrappers.AggDataTable(participant = participant, data_source = data_source).create_table()

    return True


def add_supervisor_to_campaign(supervisor: mdl.Supervisor, new_user: mdl.User) -> bool:
    """
    Binds user with campaign, making a supervisor.
    :param new_user: User object to be bound to a campaign
    :param supervisor: Supervisor object that user binds with
    :return: whether user has been bound (false if already bound)
    """

    campaign: mdl.Campaign = notnull(supervisor).campaign

    if slc.is_supervisor(user = notnull(new_user), campaign = notnull(campaign)):
        return False

    mdl.Supervisor.create(campaign = campaign, user = new_user)
    return True


def remove_supervisor_from_campaign(old_supervisor: mdl.Supervisor):
    """
    Removes a supervisor from a campaign
    :param old_supervisor: Supervisor object to be removed
    :return: None
    """

    campaign: mdl.Campaign = notnull(old_supervisor).campaign
    if old_supervisor.user != campaign.owner:
        old_supervisor.delete()


def create_campaign(
    owner: mdl.User,
    name: str,
    start_ts: datetime,
    end_ts: datetime,
    data_sources: Optional[List[mdl.DataSource]],
) -> mdl.Campaign:
    """
    Creates a campaign object in database and returns Campaign object
    :param owner: owner of the campaign
    :param name: name of the campaign
    :param start_ts: start timestamp of the campaign
    :param end_ts: end timestamp of the campaign
    :param data_sources: list of data sources to be added to the campaign
    :return: Campaign object
    """

    # 0. validate the arguments
    today = datetime.today().replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    if start_ts < today:
        raise ValueError('"start_ts" cannot be in the past!')
    if end_ts <= start_ts:
        raise ValueError('"start_ts" must be before "end_ts"!')
    if (end_ts - start_ts).days < 1:
        raise ValueError("study duration must be at least one day.")

    # 1. create a campaign
    campaign = mdl.Campaign.create(
        owner = notnull(owner),
        name = notnull(name),
        start_ts = start_ts,
        end_ts = end_ts,
    )

    # 2. add owner as a supervisor
    mdl.Supervisor.create(campaign = campaign, user = owner)

    # 3. add campaign's data sources
    if data_sources:
        for data_source in data_sources:
            add_campaign_data_source(campaign = campaign, data_source = data_source)

    return campaign


def add_campaign_data_source(campaign: mdl.Campaign, data_source: mdl.DataSource) -> bool:
    """
    Adds a data source to campaign
    :param campaign: the campaign to add data source to
    :param data_source: data source being added
    :return: whether data source has been added (false if already added)
    """

    if slc.is_campaign_data_source(campaign = campaign, data_source = data_source):
        return False

    mdl.CampaignDataSource.create(campaign = campaign, data_source = data_source)
    for participant in slc.get_campaign_participants(campaign):
        wrappers.DataTable(participant, data_source).create_table()
    return True


def remove_campaign_data_source(campaign: mdl.Campaign, data_source: mdl.DataSource):
    """
    Removes a data source from a campaign
    :param campaign: the campaign to remove data source from
    :param data_source: data source being removed
    :return: None
    """

    if not slc.is_campaign_data_source(campaign = campaign, data_source = data_source):
        return

    campaign_data_sources = mdl.CampaignDataSource.filter(
        campaign = campaign,
        data_source = data_source,
    )
    for campaign_data_source in campaign_data_sources:
        campaign_data_source.delete_instance()


def update_campaign(
    supervisor: mdl.Supervisor,
    name: str,
    start_ts: datetime,
    end_ts: datetime,
    data_sources: List[mdl.DataSource],
):
    """
    Updates a campaign
    :param supervisor: supervisor of the campaign (includes reference to user and campaign)
    :param name: new name of the campaign
    :param start_ts: new start timestamp of the campaign
    :param end_ts: new end timestamp of the campaign
    :param data_sources: new list of data sources to be added to the campaign
    :return: None
    """

    campaign: mdl.Campaign = notnull(supervisor).campaign
    campaign.name = notnull(name)
    campaign.start_ts = notnull(start_ts)
    campaign.end_ts = notnull(end_ts)
    campaign.save()

    prev_data_sources = set(slc.get_campaign_data_sources(campaign = campaign))
    cur_data_sources = set(data_sources)

    for prev_data_source in prev_data_sources.difference(cur_data_sources):
        remove_campaign_data_source(campaign = campaign, data_source = prev_data_source)

    for new_data_source in cur_data_sources.difference(prev_data_sources):
        add_campaign_data_source(campaign = campaign, data_source = new_data_source)


def delete_campaign(supervisor: mdl.Supervisor):
    """
    Deletes a campaign
    :param supervisor: supervisor of the campaign (includes reference to user and campaign)
    :return: None
    """

    campaign: mdl.Campaign = notnull(supervisor).campaign
    if supervisor.user == campaign.owner:
        campaign.delete_instance()


def create_data_source(name: str, icon_name: str, configurations: dict) -> mdl.DataSource:
    """
    Creates a data source object in database and returns DataSource object
    :param name: name of the data source
    :param icon_name: name of the icon
    :param configurations: configurations of the data source
    :return: DataSource object
    """

    data_source = mdl.DataSource.get_or_none(name = notnull(name))
    if data_source:
        return data_source

    return mdl.DataSource.create(
        name = name,
        icon_name = notnull(icon_name),
        configurations = notnull(configurations),
    )


def create_data_record(
    participant: mdl.Participant,
    data_source: mdl.DataSource,
    timestamp: datetime,
    value: Union[float, str],
):
    """
    Creates a data record in raw data table (e.g. sensor reading)
    :param participant: participant of a campaign
    :param data_source: data source of the data record
    :param ts: timestamp
    :param val: value
    :return: None
    """

    wrappers.DataTable(participant = participant, data_source = data_source).insert(
        timestamp = timestamp,
        value = value,
    )


def create_data_records(
    participant: mdl.Participant,
    data_source_ids: List[int],
    timestamps: List[datetime],
    values: List[Union[float, str]],
):
    """
    Creates a list of data records in raw data table (e.g. sensor reading)
    :param participant: participant of a campaign
    :param data_source_ids: list of data source ids
    :param tss: list of timestamps
    :param vals: list of values
    :return: None
    """

    data_sources: Dict[int, mdl.DataSource] = {}   # dict()
    for timestamp, data_source_id, value in zip(timestamps, data_source_ids, values):
        if data_source_id not in data_sources:
            db_data_source = slc.find_data_source(data_source_id = data_source_id, name = None)
            if db_data_source is None:
                continue
            data_sources[data_source_id] = db_data_source
        create_data_record(
            participant = participant,
            data_source = data_sources[data_source_id],
            timestamp = timestamp,
            value = value,
        )


def dump_data(participant: mdl.Participant, data_source: Optional[mdl.DataSource]) -> str:
    """
    Dumps data of a participant to a file
    :param participant: participant of a campaign
    :param data_source: data source to dump data from
    :return: path to the file
    """

    data_table = wrappers.DataTable(participant = participant, data_source = data_source)
    return data_table.dump_to_file()

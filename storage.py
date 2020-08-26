'''
   Copyright 2012 Will Rogers

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
   
@author Will Rogers
'''

import datetime as dt
import time
from record import Record
from xml.dom.minidom import Document
import logging

# get the relevant logger
log = logging.getLogger(__name__)


class StorageRecord(Record):
    '''
    Class to represent one storage record. 
    
    It knows about the structure of the MySQL table and the message format.
    It stores its information in a dictionary self._record_content.  The keys 
    are in the same format as in the messages, and are case-sensitive.
    '''
    
    MANDATORY_FIELDS = ["RECORD_ID", "CREATE_TIME", "STORAGE_SYSTEM",
                         "RESOURCE_CAPACITY_USED", "START_TIME", "END_TIME"]

    # This list specifies the information that goes in the database.
    DB_FIELDS = ["RECORD_ID", "CREATE_TIME", "STORAGE_SYSTEM", "STORAGE_SHARE",
                 "STORAGE_MEDIA", "STORAGE_CLASS", "FILE_COUNT", "DIRECTORY_PATH",
                 "LOCAL_USER", "LOCAL_GROUP", "USER_IDENTITY",
                 "GROUP", "GROUP_ATTRIBUTE", "GROUP_ATTRIBUTE_TYPE", "RESOURCE_CAPACITY_USED", "LOGICAL_CAPACITY_USED",
                 "START_TIME", "END_TIME", "RESOURCE_CAPACITY_ALLOCATED"]
    ALL_FIELDS = DB_FIELDS
    all_records = []

    def __init__(self):
        '''Provide the necessary lists containing message information.'''
        
        Record.__init__(self)
        
        # Fields which are required by the message format.
        self._mandatory_fields = StorageRecord.MANDATORY_FIELDS
        
        # This list specifies the information that goes in the database.
        self._db_fields = StorageRecord.DB_FIELDS
        
        # Fields which are accepted but currently ignored.
        self._ignored_fields = []
        
        self._all_fields = self._db_fields
        self._datetime_fields = ["CREATE_TIME",]

        self._duration_fields = []
        # Fields which will have an integer stored in them
        self._int_fields = ["FILE_COUNT", "RESOURCE_CAPACITY_USED", "LOGICAL_CAPACITY_USED"]
        StorageRecord.all_records.append(self)

    def get_apel_db_insert(self, source=None):
        '''
        Returns record content as a tuple, appending the source of the record 
        (i.e. the sender's DN).  Also returns the appropriate stored procedure.
       
        We have to go back to the apel_db object to find the stored procedure.
        This is because only this object knows what type of record it is,
        and only the apel_db knows what the procedure details are. 
        '''

        values = self.get_db_tuple(source)

        return values

    def get_db_tuple(self, source=None):
        """
        Return record contents as tuple ignoring the 'source' keyword argument.

        The source (DN of the sender) isn't used in this record type currently.
        """
        return Record.get_db_tuple(self)

    def get_ur(self, withhold_dns=False):
        '''
        Returns the StorageRecord in StAR format. See
        http://cds.cern.ch/record/1452920/

        Namespace information is written only once per record, by dbunloader.
        '''
        del withhold_dns  # Unused

        doc = Document()
        ur = doc.createElement('STORAGE')

        record_id = self.get_field('RECORD_ID')
        rec_id = doc.createElement('RECORD_ID')
        rec_id.appendChild(doc.createTextNode(record_id))
        ur.appendChild(rec_id)

        create_time_text = time.strftime('%Y-%m-%dT%H:%M:%SZ', self.get_field('CREATE_TIME').timetuple())

        ct = doc.createElement('CREATE_TIME')
        ct.appendChild(doc.createTextNode(create_time_text))
        ur.appendChild(ct)

        storage_system = self.get_field('STORAGE_SYSTEM')
        s_system = doc.createElement('STORAGE_SYSTEM')
        s_system.appendChild(doc.createTextNode(storage_system))
        ur.appendChild(s_system)

        if self.get_field('STORAGE_SHARE') is not None:
            storage_share = self.get_field('STORAGE_SHARE')
            s_share = doc.createElement('STORAGE_SHARE')
            s_share.appendChild(doc.createTextNode(storage_share))
            ur.appendChild(s_share)

        if self.get_field('STORAGE_MEDIA') is not None:
            storage_media = self.get_field('STORAGE_MEDIA')
            s_media = doc.createElement('STORAGE_MEDIA')
            s_media.appendChild(doc.createTextNode(storage_media))
            ur.appendChild(s_media)

        if self.get_field('STORAGE_CLASS') is not None:
            storage_class = self.get_field('STORAGE_CLASS')
            s_class = doc.createElement('STORAGE_CLASS')
            s_class.appendChild(doc.createTextNode(storage_class))
            ur.appendChild(s_class)

        if self.get_field('FILE_COUNT') is not None:
            file_count = self.get_field('FILE_COUNT')
            f_count = doc.createElement('FILE_COUNT')
            f_count.appendChild(doc.createTextNode(str(file_count)))
            ur.appendChild(f_count)

        if self.get_field('DIRECTORY_PATH') is not None:
            directory_path = self.get_field('DIRECTORY_PATH')
            d_path = doc.createElement('DIRECTORY_PATH')
            d_path.appendChild(doc.createTextNode(directory_path))
            ur.appendChild(d_path)

        # Create Subject Identity Block

        if self.get_field('LOCAL_USER') is not None:
            local_user = self.get_field('LOCAL_USER')
            l_user = doc.createElement('LOCAL_USER')
            l_user.appendChild(doc.createTextNode(local_user))
            ur.appendChild(l_user)

        if self.get_field('LOCAL_GROUP') is not None:
            local_group = self.get_field('LOCAL_GROUP')
            l_group = doc.createElement('LOCAL_GROUP')
            l_group.appendChild(doc.createTextNode(local_group))
            ur.appendChild(l_group)

        if self.get_field('USER_IDENTITY') is not None:
            user_identity = self.get_field('USER_IDENTITY')
            u_identity = doc.createElement('USER_IDENTITY')
            u_identity.appendChild(doc.createTextNode(user_identity))
            ur.appendChild(u_identity)

        if self.get_field('GROUP') is not None:
            group_field = self.get_field('GROUP')
            group_node = doc.createElement('GROUP')
            group_node.appendChild(doc.createTextNode(group_field))
            ur.appendChild(group_node)

        if self.get_field('GROUP_ATTRIBUTE') is not None:
            group_field = self.get_field('GROUP_ATTRIBUTE')
            group_node = doc.createElement('GROUP_ATTRIBUTE')
            group_node.appendChild(doc.createTextNode(group_field))
            ur.appendChild(group_node)

        if self.get_field('GROUP_ATTRIBUTE_TYPE') is not None:
            sub_attr = doc.createElement('GROUP_ATTRIBUTE_TYPE')
            sub_attr.setAttribute('GROUP_ATTRIBUTE_TYPE', 'subgroup')
            sub_attr.appendChild(doc.createTextNode(self.get_field('GROUP_ATTRIBUTE_TYPE')))
            ur.appendChild(sub_attr)

        start_time_text = time.strftime('%Y-%m-%dT%H:%M:%SZ', self.get_field('START_TIME').timetuple())
        m_time = doc.createElement('START_TIME')
        m_time.appendChild(doc.createTextNode(start_time_text))
        ur.appendChild(m_time)

        end_time_text = time.strftime('%Y-%m-%dT%H:%M:%SZ', self.get_field('END_TIME').timetuple())
        m_time = doc.createElement('END_TIME')
        m_time.appendChild(doc.createTextNode(end_time_text))
        ur.appendChild(m_time)

        resource_capacity_used = self.get_field('RESOURCE_CAPACITY_USED')
        r_capacity_used = doc.createElement('RESOURCE_CAPACITY_USED')
        r_capacity_used.appendChild(doc.createTextNode(str(resource_capacity_used)))
        ur.appendChild(r_capacity_used)

        resource_capacity_allocated = self.get_field('RESOURCE_CAPACITY_ALLOCATED')
        r_capacity_allocated = doc.createElement('RESOURCE_CAPACITY_ALLOCATED')
        r_capacity_allocated.appendChild(doc.createTextNode(str(resource_capacity_allocated)))
        ur.appendChild(r_capacity_allocated)

        if self.get_field('LOGICAL_CAPACITY_USED') is not None:
            logical_capacity_used = self.get_field('LOGICAL_CAPACITY_USED')
            l_capacity_used = doc.createElement('LOGICAL_CAPACITY_USED')
            l_capacity_used.appendChild(doc.createTextNode(str(logical_capacity_used)))
            ur.appendChild(l_capacity_used)

        doc.appendChild(ur)
        return doc.documentElement.toprettyxml()


    def output(self):
        return self.get_ur()
import time
from functools import cache
import requests


class MyClickUp:
    _count = 0
    _callsPerMinute = 100

    def __init__(self, token: str, callsPerMinute: int = 100):
        self._token = token
        self._baseUrl = "https://api.clickup.com/api/v2/"
        self._headers = {
            "Content-Type": "application/json",
            "Authorization": self._token
        }

        MyClickUp._callsPerMinute = callsPerMinute

    @staticmethod
    def _checkCounter():
        MyClickUp._count += 1

        if MyClickUp._count == MyClickUp._callsPerMinute:
            # wait for 1 minute because reached the number of calls per minute
            MyClickUp._count = 0
            time.sleep(60)

    def _apiGet(self, urlClickUp: str, params = None) -> dict:
        self._checkCounter()
        if params:
            auth_response = requests.get(urlClickUp, headers=self._headers, params=params)
        else:
            auth_response = requests.get(urlClickUp, headers=self._headers)
        return auth_response.json()

    def _apiPost(self, urlClickUp: str, json: dict) -> dict:
        self._checkCounter()
        auth_response = requests.post(urlClickUp, headers=self._headers, json=json)
        return auth_response.json()

    def _apiPut(self, urlClickUp: str, json: dict) -> dict:
        self._checkCounter()
        auth_response = requests.put(urlClickUp, headers=self._headers, json=json)
        return auth_response.json()

    def _apiDelete(self, urlClickUp: str):
        self._checkCounter()
        requests.delete(urlClickUp, headers=self._headers)

    @cache
    def getTeam(self) -> dict:
        """
        Returns a dict with the data of users registered in ClickUp. See ClickUp API documentation for details of the structure of this data.
        """
        urlClickUp = f"{self._baseUrl}team"
        return self._apiGet(urlClickUp)

    @cache
    def getSpace(self, spaceId: str) -> dict:
        """
        Returns a dict with data from a Space. See ClickUp API documentation for details of the structure of this data.
        """
        urlClickUp = f"{self._baseUrl}space/{spaceId}"
        return self._apiGet(urlClickUp)

    @cache
    def getSpaceFolders(self, spaceId: str) -> dict:
        """
        Returns a list with the Folders of a Space. See ClickUp API documentation for details of the structure of this data.
        """
        urlClickUp = f"{self._baseUrl}space/{spaceId}/folder"
        return self._apiGet(urlClickUp)

    @cache
    def getFolder(self, folderId: str) -> dict:
        """
        Returns a dict with data from a Folder. See ClickUp API documentation for details of the structure of this data.
        """
        urlClickUp = f"{self._baseUrl}folder/{folderId}"
        return self._apiGet(urlClickUp)

    @cache
    def getFolderByName(self, folderName: str, spaceId) -> list:
        """
        Returns a list with the Folders of a Space. See ClickUp API documentation for details of the structure of this data.
        """
        folderName = folderName.lower()
        folderList = []
        mySpace = self.getSpaceFolders(spaceId)
        for myFolder in mySpace['folders']:
            if myFolder['name'].lower() == folderName:
                folderList.append(myFolder)
            # endif --
        # endfor --
        return folderList

    @cache
    def getFolderLists(self, folderId: str) -> dict:
        """
        Returns a list with the Lists of a Folder. See ClickUp API documentation for details of the structure of this data.
        """
        urlClickUp = f"{self._baseUrl}folder/{folderId}/list"
        return self._apiGet(urlClickUp)

    @cache
    def getList(self, listId: str) -> dict:
        """
        Returns a dict with data from a List. See ClickUp API documentation for details of the structure of this data.
        """
        urlClickUp = f"{self._baseUrl}list/{listId}"
        return self._apiGet(urlClickUp)

    @cache
    def getListsByName(self, listName: str, folderId) -> list:
        """
        Returns a dict with data from a List. See ClickUp API documentation for details of the structure of this data.
        """
        listName = listName.lower()
        listList = []
        myFolder = self.getFolderLists(folderId)
        for myList in myFolder['lists']:
            if myList['name'].lower() == listName:
                listList.append(myList)
            # endif --
        # endfor --
        return listList

    @cache
    def getListTasks(self, listId: str) -> dict:
        """
        Returns a list with the Tasks of a List. See ClickUp API documentation for details of the structure of this data.
        """
        urlClickUp = f"{self._baseUrl}list/{listId}/task"
        return self._apiGet(urlClickUp)

    @cache
    def getTask(self, taskId: str, flagSubtasks: bool = False) -> dict:
        """
        Returns a dict with data from a Task. See ClickUp API documentation for details of the structure of this data.
        """
        urlClickUp = f"{self._baseUrl}task/{taskId}"
        params = {"subtasks": flagSubtasks}
        return self._apiGet(urlClickUp, params=params)

    @cache
    def getTasksByName(self, taskName: str, listId) -> list:
        """
        Returns a dict with data from a Task. See ClickUp API documentation for details of the structure of this data.
        """
        taskName = taskName.lower()
        taskList = []
        myList = self.getListTasks(listId)
        for myTask in myList['tasks']:
            if myTask['name'].lower() == taskName:
                taskList.append(myTask)
            # endif --
        # endfor --
        return taskList

    @cache
    def getListCustomFields(self, listId: str) -> dict:
        """
        Returns a list with the Custom Fields of a List. See ClickUp API documentation for details of the structure of this data.
        """
        urlClickUp = f"{self._baseUrl}list/{listId}/field"
        return self._apiGet(urlClickUp)

    @cache
    def getListCustomFieldByName(self, listId: str, fieldName: str) -> dict | None:
        """
        Returns a dict with the details of a Custom Fields of a List. See ClickUp API documentation for details of the structure of this data.
        """
        fieldName = fieldName.lower()
        customFields = self.getListCustomFields(listId)
        if 'fields' in customFields:
            for field in customFields['fields']:
                if field['name'].lower() == fieldName:
                    return field
                # endif --
            # endfor --
        # endif --
        return None

    @cache
    def getCustomFieldOption(self, listId: str, fieldName: str, optionName: str) -> dict | None:
        """
        Returns a list with the options of a Custom Fields of a List. See ClickUp API documentation for details of the structure of this data.
        """
        field = self.getListCustomFieldByName(listId=listId, fieldName=fieldName)
        if not field or 'type_config' not in field or 'options' not in field['type_config']:
            return None
        # endif --
        optionName = optionName.lower()
        for option in field['type_config']['options']:
            if option['name'].lower() == optionName:
                return option
            # endif --
        # endfor --
        return None

    @cache
    def getUser(self, userId: str) -> dict:
        """
        Returns a dict with a Users's data. See ClickUp API documentation for details of the structure of this data.
        """
        urlClickUp = f"{self._baseUrl}team/team_id/user/{userId}"
        return self._apiGet(urlClickUp)

    def createFolder(self, folderJson: dict, spaceId: str) -> dict:
        """
        Creates a Folder in a given Space, the Folder details are specified in the dict "folderJson", according to the ClickUp API . See ClickUp API documentation for details of the structure of this data.
        """
        urlClickUp = f"{self._baseUrl}space/{spaceId}/folder"
        return self._apiPost(urlClickUp, json=folderJson)

    def createList(self, listJson: dict, folderId: str) -> dict:
        """
        Creates a List in a given Folder, the List details are specified in the dict "listJson", according to the ClickUp API. See ClickUp API documentation for details of the structure of this data.
        """
        urlClickUp = f"{self._baseUrl}folder/{folderId}/list"
        return self._apiPost(urlClickUp, json=listJson)

    def createTask(self, taskJson: dict, listId: str, parentTaskId: str = None) -> dict:
        """
        Creates a Task in a given Folder, the Task details are specified in the dict "taskJson", according to the ClickUp API. See ClickUp API documentation for details of the structure of this data.
        """
        if parentTaskId is not None:
            taskJson["parent"] = parentTaskId
        urlClickUp = f"{self._baseUrl}list/{listId}/task"
        return self._apiPost(urlClickUp, json=taskJson)

    def updateFolder(self, folderJson: dict, folderId: str) -> dict:
        """
        Updates the Folder properties, the Folder details are specified in the dict "folderJson", according to the ClickUp API. See ClickUp API documentation for details of the structure of this data.
        """
        urlClickUp = f"{self._baseUrl}folder/{folderId}"
        return self._apiPut(urlClickUp, json=folderJson)

    def updateList(self, listJson: dict, listId: str) -> dict:
        """
        Updates the List properties, the List details are specified in the dict "listJson", according to the ClickUp API. See ClickUp API documentation for details of the structure of this data.
        """
        urlClickUp = f"{self._baseUrl}list/{listId}"
        return self._apiPut(urlClickUp, json=listJson)

    def updateTask(self, taskJson: dict, taskId: str) -> dict:
        """
        Updates the Task properties, the Task details are specified in the dict "taskJson", according to the ClickUp API. See ClickUp API documentation for details of the structure of this data.
        """
        urlClickUp = f"{self._baseUrl}task/{taskId}"
        return self._apiPut(urlClickUp, json=taskJson)

    def deleteFolder(self, folderId: str):
        """
        Delete a Folder. See ClickUp API documentation for details of the structure of this data.
        """
        urlClickUp = f"{self._baseUrl}folder/{folderId}"
        self._apiDelete(urlClickUp)

    def deleteList(self, listId: str):
        """
        Delete a List. See ClickUp API documentation for details of the structure of this data.
        """
        urlClickUp = f"{self._baseUrl}list/{listId}"
        self._apiDelete(urlClickUp)

    def deleteTask(self, taskId: str):
        """
        Delete a Task. See ClickUp API documentation for details of the structure of this data.
        """
        urlClickUp = f"{self._baseUrl}task/{taskId}"
        self._apiDelete(urlClickUp)
# endclass --

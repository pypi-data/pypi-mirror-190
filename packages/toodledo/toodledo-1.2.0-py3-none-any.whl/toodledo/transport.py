"""Implementation"""

from json import dumps
from logging import debug, error, warning

from requests_oauthlib import OAuth2Session

from .account import _AccountSchema
from .context import _ContextSchema
from .errors import ToodledoError
from .folder import _FolderSchema
from .task import _DumpTaskList, _TaskSchema


class AuthorizationNeeded(Exception):
    """Thrown when the token storage doesn't contain a token"""


class ToodledoSession(OAuth2Session):
    """Refresh token when we get a 429 error"""
    def __init__(self, *args, **kwargs):
        self.refreshing = False
        super().__init__(*args, **kwargs)

    def request(self, *args, **kwargs):  # pylint: disable=too-many-arguments
        response = super().request(*args, **kwargs)
        if response.status_code != 429:
            self.refreshing = False
            return response
        if self.refreshing:
            response.raise_for_status()
        self.refreshing = True
        warning("Received 429 error - refreshing token and retrying")
        token = self.refresh_token(
            Toodledo.tokenUrl, **self.auto_refresh_kwargs)
        self.token_updater(token)
        return super().request(*args, **kwargs)


class Toodledo:
    """Wrapper for the Toodledo v3 API"""
    baseUrl = "https://api.toodledo.com/3/"
    tokenUrl = baseUrl + "account/token.php"
    getAccountUrl = baseUrl + "account/get.php"
    getTasksUrl = baseUrl + "tasks/get.php"
    deleteTasksUrl = baseUrl + "tasks/delete.php"
    addTasksUrl = baseUrl + "tasks/add.php"
    editTasksUrl = baseUrl + "tasks/edit.php"
    getFoldersUrl = baseUrl + "folders/get.php"
    addFolderUrl = baseUrl + "folders/add.php"
    deleteFolderUrl = baseUrl + "folders/delete.php"
    editFolderUrl = baseUrl + "folders/edit.php"
    getContextsUrl = baseUrl + "contexts/get.php"
    addContextUrl = baseUrl + "contexts/add.php"
    editContextUrl = baseUrl + "contexts/edit.php"
    deleteContextUrl = baseUrl + "contexts/delete.php"

    def __init__(self, clientId, clientSecret, tokenStorage, scope):
        self.tokenStorage = tokenStorage
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.scope = scope

    def _Session(self):
        token = self.tokenStorage.Load()
        if token is None:
            raise AuthorizationNeeded("No token in storage")

        return ToodledoSession(
            client_id=self.clientId,
            token=token,
            auto_refresh_kwargs={
                "client_id": self.clientId,
                "client_secret": self.clientSecret
            },
            auto_refresh_url=Toodledo.tokenUrl,
            token_updater=self.tokenStorage.Save)

    def GetFolders(self):
        """Get all the folders as folder objects"""
        folders = self._Session().get(Toodledo.getFoldersUrl)
        folders.raise_for_status()
        schema = _FolderSchema()
        return [schema.load(x) for x in folders.json()]

    def AddFolder(self, folder):
        """Add folder, return the created folder"""
        response = self._Session().post(
            Toodledo.addFolderUrl,
            data={
                "name": folder.name,
                "private": 1 if folder.private else 0
            })
        response.raise_for_status()
        if "errorCode" in response.json():
            error(f"Toodledo error: {response.json()}")
            raise ToodledoError(response.json()["errorCode"])
        return _FolderSchema().load(response.json()[0])

    def DeleteFolder(self, folder):
        """Delete folder"""
        response = self._Session().post(Toodledo.deleteFolderUrl,
                                        data={"id": folder.id_})
        response.raise_for_status()
        jsonResponse = response.json()
        if "errorCode" in jsonResponse:
            error(f"Toodledo error: {jsonResponse}")
            raise ToodledoError(jsonResponse["errorCode"])
        assert jsonResponse == {"deleted": folder.id_}, dumps(jsonResponse)

    def EditFolder(self, folder):
        """Edits the given folder to have the given properties"""
        folderData = _FolderSchema().dump(folder)
        response = self._Session().post(Toodledo.editFolderUrl,
                                        data=folderData)
        response.raise_for_status()
        responseAsDict = response.json()
        if "errorCode" in responseAsDict:
            error(f"Toodledo error: {responseAsDict}")
            raise ToodledoError(responseAsDict["errorCode"])
        return _FolderSchema().load(responseAsDict[0])

    def GetContexts(self):
        """Get all the contexts as context objects"""
        contexts = self._Session().get(Toodledo.getContextsUrl)
        contexts.raise_for_status()
        schema = _ContextSchema()
        return [schema.load(x) for x in contexts.json()]

    def AddContext(self, context):
        """Add context, return the created context"""
        response = self._Session().post(
            Toodledo.addContextUrl,
            data={
                "name": context.name,
                "private": 1 if context.private else 0
            })
        response.raise_for_status()
        if "errorCode" in response.json():
            error(f"Toodledo error: {response.json()}")
            raise ToodledoError(response.json()["errorCode"])
        return _ContextSchema().load(response.json()[0])

    def DeleteContext(self, context):
        """Delete context"""
        response = self._Session().post(
            Toodledo.deleteContextUrl, data={"id": context.id_})
        response.raise_for_status()
        jsonResponse = response.json()
        if "errorCode" in jsonResponse:
            error(f"Toodledo error: {jsonResponse}")
            raise ToodledoError(jsonResponse["errorCode"])
        assert jsonResponse == {"deleted": context.id_}, dumps(jsonResponse)

    def EditContext(self, context):
        """Edits the given folder to have the given properties"""
        contextData = _ContextSchema().dump(context)
        response = self._Session().post(
            Toodledo.editContextUrl, data=contextData)
        response.raise_for_status()
        responseAsDict = response.json()
        if "errorCode" in responseAsDict:
            error(f"Toodledo error: {responseAsDict}")
            raise ToodledoError(responseAsDict["errorCode"])
        return _ContextSchema().load(responseAsDict[0])

    def GetAccount(self):
        """Get the Toodledo account"""
        accountInfo = self._Session().get(Toodledo.getAccountUrl)
        accountInfo.raise_for_status()
        return _AccountSchema().load(accountInfo.json())

    def GetTasks(self, params):
        """Get the tasks filtered by the given params"""
        allTasks = []
        limit = 1000  # single request limit
        start = 0
        while True:
            debug(f"Start: {start}")
            params["start"] = start
            params["num"] = limit
            response = self._Session().get(Toodledo.getTasksUrl, params=params)
            response.raise_for_status()
            tasks = response.json()
            if "errorCode" in tasks:
                error(f"Toodledo error: {tasks}")
                raise ToodledoError(tasks["errorCode"])
            # the first field contains the count or the error code
            allTasks.extend(tasks[1:])
            debug(f"Retrieved {len(tasks[1:]):,} tasks")
            if len(tasks[1:]) < limit:
                break
            start += limit
        schema = _TaskSchema()
        return [schema.load(x) for x in allTasks]

    def EditTasks(self, taskList):
        """Change the existing tasks to be the same as the ones in the given
        list"""
        if len(taskList) == 0:
            return
        debug(f"Total tasks to edit: {len(taskList)}")
        limit = 50  # single request limit
        start = 0
        while True:
            debug(f"Start: {start}")
            listDump = _DumpTaskList(taskList[start:start + limit])
            response = self._Session().post(
                Toodledo.editTasksUrl, data={"tasks": dumps(listDump)})
            response.raise_for_status()
            debug(f"Response: {response},{response.text}")
            taskResponse = response.json()
            errors = []
            if isinstance(taskResponse, list):
                for response in taskResponse:
                    if "errorCode" in response:
                        errors.append(ToodledoError(response["errorCode"]))
            elif "errorCode" in taskResponse:
                errors.append(ToodledoError(taskResponse["errorCode"]))
            if len(errors) == 1:
                raise errors[0]
            if errors:
                # pylint: disable=broad-exception-raised
                raise Exception(str(errors))
                # pylint: enable=broad-exception-raised
            if len(taskList[start:start + limit]) < limit:
                break
            start += limit

    def AddTasks(self, taskList):
        """Add the given tasks"""
        if len(taskList) == 0:
            return
        limit = 50  # single request limit
        start = 0
        while True:
            debug(f"Start: {start}")
            listDump = _DumpTaskList(taskList[start:start + limit])
            response = self._Session().post(
                Toodledo.addTasksUrl, data={"tasks": dumps(listDump)})
            response.raise_for_status()
            taskResponse = response.json()
            errors = []
            if isinstance(taskResponse, list):
                for response in taskResponse:
                    if "errorCode" in response:
                        errors.append(ToodledoError(response["errorCode"]))
            elif "errorCode" in taskResponse:
                errors.append(ToodledoError(taskResponse["errorCode"]))
            if len(errors) == 1:
                raise errors[0]
            if errors:
                # pylint: disable=broad-exception-raised
                raise Exception(str(errors))
                # pylint: enable=broad-exception-raised
            if len(taskList[start:start + limit]) < limit:
                break
            start += limit

    def DeleteTasks(self, taskList):
        """Delete the given tasks"""
        if len(taskList) == 0:
            return
        taskIdList = [task.id_ for task in taskList]
        limit = 50  # single request limit
        start = 0
        while True:
            debug(f"Start: {start}")
            response = self._Session().post(
                Toodledo.deleteTasksUrl,
                data={
                    "tasks": dumps(taskIdList[start:start + limit])
                })
            response.raise_for_status()
            if "errorCode" in response.json():
                raise ToodledoError(response.json()["errorCode"])
            if len(taskIdList[start:start + limit]) < limit:
                break
            start += limit

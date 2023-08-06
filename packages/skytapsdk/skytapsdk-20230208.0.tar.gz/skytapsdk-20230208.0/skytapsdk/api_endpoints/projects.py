"""Environments Class for calling "configurations" API endpoints."""
import logging

from restfly.endpoint import APIEndpoint

from skytapsdk.helpers import links_iterator


class Projects(APIEndpoint):
    """
    "projects" API endpoint

    API Doc Reference: https://help.skytap.com/API_v2_Documentation.html#Project
    """

    _path = "projects"

    def get_all(self, **kwargs) -> list:
        """
        Get all project records based on query parameters sent in kwargs.

        API Doc Reference: https://help.skytap.com/API_v2_Documentation.html#Listprojects

        Returns:
            list of all projects, per set params in kwargs.
        """
        return links_iterator(api=self._api, path=self._path, **kwargs)

    def get_by_id(self, uid: int) -> dict:
        """
        GET a specific project.

        API Doc Reference: https://help.skytap.com/API_v2_Documentation.html#Getprojectdescription

        Args:
            uid: ID of desired project.

        Returns:
            dict of queried project.
        """
        self._path = f"{self._path}/{uid}.json"
        return self._get().json()

    def delete_by_id(self, uid: int) -> dict:
        """
        DELETE a specific project.

        API Doc Reference: https://help.skytap.com/API_Documentation.html#Deleteproject

        Args:
            uid: ID of desired project.

        Returns:
            dict of result.
        """
        logging.warning(
            "The delete method for Projects is an API Version 1 only feature."
        )
        self._path = f"{self._path}/{uid}"
        return self._delete()

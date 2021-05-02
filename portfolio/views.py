from fastapi import Body, Depends

# from .models import (
#     Mock,
#     DamnAPIMock,
#     APIMock,
#     APIMocks,
#     AdminUser,
#     )
# from .utils import (
#     get_mock,
#     get_user,
#     )

# def mocks_get(user: AdminUser = Depends(get_user)) -> APIMocks:
#     """
#     Return a list of available mocks-
#     """
#     mocks = user.mock_set.all()
#     api_mocks = [APIMock.from_model(m) for m in mocks]
#     return APIMocks(items=api_mocks)

# def mock_post(
#     apimock: DamnAPIMock,
#     user: AdminUser = Depends(get_user),
# ) -> APIMock:
#     """
#     Create a new mock.
#     """
#     m = Mock.from_api(user, apimock)
#     m.save()
#     return APIMock.from_model(m)

# def mock_get(
#     mock: Mock = Depends(get_mock),
#     user: AdminUser = Depends(get_user)
# ) -> APIMock:
#     """
#     Return a specific mock object.
#     """
#     return APIMock.from_model(mock)

# def mock_put(
#     mock: Mock = Depends(get_mock),
#     mock_body: DamnAPIMock = Body(...),
#     user: AdminUser = Depends(get_user),
# ) -> APIMock:
#     """
#     Update a mock
#     """
#     mock.update_from_api(mock_body)
#     mock.save()
#     return APIMock.from_model(mock)

# def mock_delete(
#     mock: Mock = Depends(get_mock),
#     user: AdminUser = Depends(get_user)
# ) -> APIMock:
#     """
#     Delete a mock.
#     """
#     d = APIMock.from_model(mock)
#     mock.delete()
#     return d
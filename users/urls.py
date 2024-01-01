# Django
from django.urls import path

# View
from users import views


urlpatterns = [

    # Management
    path(
        route='login/',
        view=views.LoginView.as_view(),
        name='login'
    ),
    path(
        route='logout/',
        view=views.LogoutView.as_view(),
        name='logout'
    ),
    path(
        route='signup/',
        view=views.SignupView.as_view(),
        name='signup'
    ),
    path(
        route='me/profile/',
        view=views.UpdateProfileView.as_view(),
        name='update'
    ),
    path(
        route='me/records_status/',
        view=views.RecordsStatusView.as_view(),
        name='records_status'
    ),
    path(
        route='<int:user>/',
        view=views.UserDetailView.as_view(),
        name='detail'
    ),
    path(
        route='<str:username>/',
        view=views.UserDetailView2.as_view(),
        name='detail2'
    )

]
from django.urls import path
from . import views
from heart_charity import views



urlpatterns = [

    path("", views.home, name="home"),  # Home page
    path('signup/', views.signup_view, name='signup'),
    path('signin', views.signin_view, name='signin'),
    path("our_causes/",views.our_causes,name="our_causes"),
    path("logout", views.logout_view, name="logout"),  # Logout page
    path(
        "request_password_reset/",
        views.request_password_reset,
        name="request_password_reset",
    ),
    path("reset_password/<uname>/", views.reset_password, name="reset_password"),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('volunteer-dashboard/', views.volunteer_dashboard, name='volunteer_dashboard'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    # path("issue_item/", views.issue_item, name="issue_item"),  # Book issue page
    # path("signin/", views.login_user, name="signin"),  # Login page
    # path("register", views.register, name="register"),  # Registration page
    # path("logout", views.logout_view, name="logout"),  # Logout page
    # path("return_item", views.return_item, name="return_item"),  # Return item page
    
    # path("history", views.history, name="history"),  # History page for issued book
    # path(
    #     "request_password_reset/",
    #     views.request_password_reset,
    #     name="request_password_reset",
    # ),
    # path("reset_password/<uname>/", views.reset_password, name="reset_password"),
    # path('searchproduct/',views.searchproduct,name='searchproduct'),
    # path('searchproductstudy/',views.searchproductstudy,name='searchproductstudy'),
    # path('searchproductreturn/',views.searchproductreturn,name='searchproductreturn'),
    # path('submit/', views.submit_return_date, name='submit_return_date'),
    # path("contact_view/", views.contact_view, name="contact_view"),
    # path('study-materials/', views.study_material_list, name='study_material_list'),
    # path('readers/', views.readers, name='readers'),
    # path('searchproductreaders/', views.searchproductreaders, name='searchproductreaders'),
    # path('payment_reader/<int:reader_id>/', views.payment_reader, name='payment_reader'),
    # path('payment',views.payment,name='payment'),
    # path('expected_book/',views.expected_book,name='expected_book'),
    # path('del/<str:item_id>', views.remove, name="del"),
    # path('admin/', admin.site.urls),
] 

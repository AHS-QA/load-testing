from asyncio import events
from locust import HttpLocust, TaskSet, task
import time
import json
import inspect
from additional_handlers import additional_success_handler, additional_failure_handler

events.request_success += additional_success_handler
events.request_failure += additional_failure_handler


def custom_timer(func):

    def func_wrapper(*args, **kwargs):
        """ wrap functions and measure time """

        previous_frame = inspect.currentframe().f_back
        (filename, line_number, function_name, lines, index) = inspect.getframeinfo(previous_frame)

        start_time = time.time()
        result = None
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="CUSTOM", name=func.__name__,
                                        response_time=total_time, exception=e, tag=function_name)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="CUSTOM", name=func.__name__,
                                        response_time=total_time, response_length=0, tag=function_name)
        return result

    return func_wrapper


class UserBehavior(TaskSet):

    def on_start(self):
        self.log_in()

    def on_stop(self):
        self.log_out()

    @custom_timer
    def log_in(self):
        with open('data.json') as f:
            data = json.load(f)
            self.client.post("/Account/Login", {
                "MainContent_Username": data['mp_login']['uid'],
                "MainContent_MainContent_Password": data['win_login']['pwd']
            })

    @custom_timer
    def log_out(self):
        with open('data.json') as f:
            data = json.load(f)
            self.client.post("/Account/Logout", {
                "MainContent_Username": data['mp_login']['uid'],
                "MainContent_MainContent_Password": data['win_login']['pwd']
            })

    # Account registration
    @task(2)
    @custom_timer
    def register(self):
        self.client.get("/Account/Register")

    # Account management options
    @task(1)
    @custom_timer
    def my_account(self):
        self.client.get("/App/AccountManage/myAccount.html?v=2019.6.4.1")

    @task(1)
    @custom_timer
    def change_password(self):
        self.client.get("/app/accountmanage/changepassword.html?v=2019.6.4.1")

    # Site pages
    @task(4)
    @custom_timer
    def index(self):
        self.client.get("/app/home/home.html?v=2019.6.4.1")
        print("home")

    @task(4)
    @custom_timer
    def add_member(self):
        self.client.get("/app/members/addMember.html?v=2019.6.4.1")
        print("add member")

    @task(2)
    @custom_timer
    def view_members(self):
        self.client.get("/App/Members/members.html?v=2019.6.4.1")

    @task(2)
    @custom_timer
    def complaints_process(self):
        self.client.get("/App/Complaint/complaintInbox.html?v=2019.6.4.1")
        # time.sleep(3)
        self.client.get("/App/Complaint/Wizard/complainantContactInfo.html?v=2019.6.4.1")
        self.client.get("/App/Complaint/Wizard/allegations.html?v=2019.6.4.1")
        self.client.get("/App/Complaint/Wizard/complaintReview.html?v=2019.6.4.1")
        self.client.get("/App/Complaint/Parts/complaintView.directive.html?v=2019.6.4.1")
        self.client.get("/App/Complaint/Parts/createEditIssue.directive.html?v=2019.6.4.1")
        self.client.get("/App/Complaint/Parts/issueView.directive.html?v=2019.6.4.1")
        print("complaints process")

    @task(4)
    @custom_timer
    def enrollment_process(self):
        self.client.get("/App/SMMCEnrollmentWizard/Wizard/Shared/selectMember.html?v=2019.6.4.1")
        self.client.get("/App/SMMCEnrollmentWizard/Directives/Shared/selectMemberCard.directive.html?v=2019.6.4.1")
        self.client.get("/App/SMMCEnrollmentWizard/Directives/Shared/selectMemberCardPanel.directive.html?v=2019.6.4.1")
        self.client.get("/app/script/ahsScript.directive.html?v=2019.6.4.1")
        self.client.get("/App/Layout/personWizardPanel.directive.html?v=2019.6.4.1")
        self.client.get("/App/Layout/wizardAccordian.directive.html?v=2019.6.4.1")
        self.client.get("/App/SMMCEnrollmentWizard/Wizard/Shared/selectHealthPlanChangeReason.html?v=2019.6.4.1")
        self.client.get("/App/SMMCEnrollmentWizard/Wizard/Dental/selectDentalPlanChangeReason.html?v=2019.6.4.1")
        self.client.get("/App/SMMCEnrollmentWizard/Directives/Shared/selectSpecialNeedList.directive.html?v=2019.6.4.1")
        # self.client.get("/App/SMMCEnrollmentWizard/Directives/Shared/selectCMS.directive.html?v=2019.6.4.1")
        self.client.get("/App/SMMCEnrollmentWizard/Wizard/Shared/selectHealthPlan.html?v=2019.6.4.1")
        self.client.get("/App/SMMCEnrollmentWizard/Wizard/Dental/selectDentalPlan.html?v=2019.6.4.1")
        self.client.get("/App/SMMCChoiceTools/sMMCAvailableHealthPlanGrid.directive.html?v=2019.6.4.1")
        self.client.get("/App/SMMCEnrollmentWizard/Directives/Shared/selectSubmitReviewHealthPlanPanel.html?v=2019.6.4.1")
        self.client.get("/App/SMMCEnrollmentWizard/Directives/Dental/selectSubmitReviewDentalPlanPanel.html?v=2019.6.4.1")
        self.client.get("/app/script/ahsScriptQuestionControl.directive.html?v=2019.6.4.1")
        self.client.get("/app/script/ahsScriptSummary.directive.html?v=2019.6.4.1")
        self.client.get("/app/script/ahsScript.directive.html?v=2019.6.4.1")
        print("enrollment process")

    @task(1)
    @custom_timer
    def mail_history(self):
        self.client.get("/App/Mail/mailHistory.html?v=2019.6.4.1")


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    host = "https://membersqa.flmedicaidmanagedcare.com"
    min_wait = 5000
    max_wait = 15000

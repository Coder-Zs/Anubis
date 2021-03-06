from anubis.model import builtin


class Error(Exception):
    pass


class HashError(Error):
    pass


class InvalidStateError(Error):
    pass


class UserFacingError(Error):
    def to_dict(self):
        return {'name': self.__class__.__name__, 'args': self.args, 'message': self.message.format(*self.args)}

    @property
    def http_status(self):
        return 500

    @property
    def template_name(self):
        return 'error.html'

    @property
    def message(self):
        return 'An error has occurred.'


class ForbiddenError(UserFacingError):
    @property
    def http_status(self):
        return 403


class NotFoundError(UserFacingError):
    @property
    def http_status(self):
        return 404

    @property
    def message(self):
        return 'path {0} not found.'


class InvalidTeacherError(InvalidStateError):
    pass


class BuiltinDomainError(ForbiddenError):
    @property
    def message(self):
        return 'Domain {0} is built-in and cannot be modified.'


class ValidationError(ForbiddenError):
    @property
    def message(self):
        if len(self.args) == 1:
            return 'Field {0} validation failed.'
        elif len(self.args) == 2:
            return 'Field {0} or {1} validation failed.'


class FileTooLongError(ValidationError):
    @property
    def message(self):
        return 'The uploaded file is too long.'


class FileTypeNotAllowedError(ValidationError):
    @property
    def message(self):
        return 'This type of files are not allowed to be uploaded.'


class UnknownFieldError(ForbiddenError):
    @property
    def message(self):
        return 'Unknown field {0}.'


class InvalidTokenError(ForbiddenError):
    pass


class VerifyPasswordError(ForbiddenError):
    # Error with the `VERIFY PASSWORD` , not password verification error.
    @property
    def message(self):
        return 'Passwords don\'t match.'


class UserAlreadyExistError(ForbiddenError):
    @property
    def message(self):
        return 'User {0} already exists.'


class LoginError(ForbiddenError):
    @property
    def message(self):
        return 'Invalid password for user {0}.'


class DocumentNotFoundError(NotFoundError):
    @property
    def message(self):
        return 'Document {1} not found.'


class ProblemDataNotFoundError(NotFoundError):
    @property
    def message(self):
        return 'Data of problem {1} not found.'


class RecordDataNotFoundError(NotFoundError):
    @property
    def message(self):
        return 'Data of record {1} not found.'


class PermissionError(ForbiddenError):
    @property
    def message(self):
        if any((p | builtin.PERM_VIEW) == builtin.PERM_VIEW for p in self.args):
            return 'You cannot visit this domain.'
        else:
            if len(self.args) > 0 and self.args[0] in builtin.PERMS_BY_KEY:
                self.args = (builtin.PERMS_BY_KEY[self.args[0]].desc, self.args[0], *self.args[1:])
            return "You don't have the required permission ({0}) in this domain."


class PrivilegeError(ForbiddenError):
    @property
    def message(self):
        if any((p | builtin.PRIV_USER_PROFILE) == builtin.PRIV_USER_PROFILE for p in self.args):
            return "You're not logged in."
        else:
            return "You don't have the required privilege."


class CsrfTokenError(ForbiddenError):
    pass


class InvalidOperationError(ForbiddenError):
    pass


class AlreadyVotedError(ForbiddenError):
    @property
    def message(self):
        return "You're already voted."


class UserNotFoundError(ForbiddenError):
    @property
    def message(self):
        return 'User not found.'


class InvalidTokenDigestError(ForbiddenError):
    pass


class CurrentPasswordError(ForbiddenError):
    @property
    def message(self):
        return "Current password doesn't match."


class DiscussionCategoryAlreadyExistError(ForbiddenError):
    @property
    def message(self):
        return "Discussion category {1} already exists."


class DiscussionCategoryNotFoundError(NotFoundError):
    @property
    def message(self):
        return "Discussion category {1} not found."


class DiscussionNodeAlreadyExistError(ForbiddenError):
    @property
    def message(self):
        return "Discussion Node {1} already exists."


class DiscussionNodeNotFoundError(NotFoundError):
    @property
    def message(self):
        return 'Discussion node {1} not found.'


class DiscussionNotFoundError(DocumentNotFoundError):
    @property
    def message(self):
        return 'Discussion {1} not found.'


class MessageNotFoundError(NotFoundError):
    @property
    def message(self):
        return 'Message {0} not found.'


class DomainNotFoundError(NotFoundError):
    @property
    def message(self):
        return 'Domain {0} not found.'


class DomainAlreadyExistError(ForbiddenError):
    @property
    def message(self):
        return 'Domain {0} already exists.'


class ContestAlreadyAttendedError(ForbiddenError):
    @property
    def message(self):
        return "You've already attended this contest."


class ContestNotFoundError(NotFoundError):
    @property
    def message(self):
        return 'Contest {1} not found.'


class ContestNotAttendedError(ForbiddenError):
    @property
    def message(self):
        return "You haven't attended this contest yet."


class ContestStatusHiddenError(ForbiddenError):
    @property
    def message(self):
        return "Contest status is hidden."


class ContestIllegalBalloonError(ForbiddenError):
    @property
    def message(self):
        return "This balloon can't be send."


class ContestNotLiveError(ForbiddenError):
    @property
    def message(self):
        return "This contest is not live."


class ContestIsPrivateError(ForbiddenError):
    @property
    def message(self):
        return 'This contest is private.'


class UserFileNotFoundError(NotFoundError):
    @property
    def message(self):
        return 'File {0} not found.'


class ProblemNotFoundError(NotFoundError):
    @property
    def message(self):
        return 'Problem {1} not found.'


class ProblemCannotPretestError(ForbiddenError):
    @property
    def message(self):
        return "Problem {0} can't be pretested."


class ContestProblemNotFoundError(NotFoundError):
    @property
    def message(self):
        return 'Problem {0} not found.'


class TrainingRequirementNotSatisfiedError(ForbiddenError):
    @property
    def message(self):
        return 'Training requirement is not satisfied.'


class RecordNotFoundError(NotFoundError):
    @property
    def message(self):
        return 'Record {0} not found.'


class OpCountExceededError(ForbiddenError):
    @property
    def message(self):
        return 'Too frequent operations of {0} (Limit: {2} operations in {1} seconds.).'


class UsageExceedError(ForbiddenError):
    @property
    def message(self):
        return 'Usage exceeded.'


class CampaignAlreadyExistError(ForbiddenError):
    @property
    def message(self):
        return 'Campaign {0} already exists.'


class CampaignTeamAlreadyExistError(ForbiddenError):
    @property
    def message(self):
        return 'Member {0} already exists.'


class CampaignTeamNotFoundError(NotFoundError):
    @property
    def message(self):
        return 'Team {1} in campaign {0} not found.'


class CampaignNotInTimeError(ForbiddenError):
    @property
    def message(self):
        return 'Campaign {0} is not in attend time.'


class StudentFetchError(ForbiddenError):
    @property
    def message(self):
        return 'Student {0} fetch failed.'


class StudentIsNotNewbieError(ForbiddenError):
    @property
    def message(self):
        return 'Student {0} is not newbie.'


class StudentNotFoundError(NotFoundError):
    @property
    def message(self):
        return 'Student {0} not found.'

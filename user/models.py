from django.db import models
from django import forms
from django.conf import settings
from django.utils import timezone

class User(models.Model):
    userid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    email = models.EmailField()
    nickname = models.CharField(max_length=128)
    password = models.CharField(max_length=255)
    sex = models.CharField('性别', max_length=12, default='')
    birthday = models.CharField('生日', max_length=32, default='')
    location = models.CharField('所在地', max_length=32, default="中国大陆")
    avatar_url = models.CharField('用户头像路径', max_length=128, default='')
    avatar = models.FileField('用户头像', upload_to='')
    last_login = models.DateTimeField('最后登录时间',default=timezone.now)
    # join = models.ManyToManyField('self', through='Join', symmetrical=False, related_name='joined_by')
    class Meta:
        db_table = 'User'

    def to_dic(self):
        return {
            "id": self.userid,
            "username": self.username,
            "email": self.email,
            'nickname': self.nickname,
            'sex': self.sex,
            'birthday': self.birthday,
            'location': self.location,
            "avatar_url": self.avatar_url,
        }

    def __str__(self):
        return self.username


class Team(models.Model):
    teamid = models.AutoField(primary_key=True)
    teamname = models.CharField(max_length=255)
    creatorid = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Team'  # 改变当前模型类对应的表名

    def to_dic(self):
        return {
            "teamid": self.teamid,
            "teamname": self.teamname,
            "creatorid": self.creatorid.userid
        }

    def __str__(self):
        return self.username


class UserToTeam(models.Model):
    userid = models.IntegerField(verbose_name='主体', default=0)
    teamid = models.IntegerField(verbose_name='团队', default=0)


class TeamToUser(models.Model):
    teamid = models.IntegerField(verbose_name='主体', default=0)
    userid = models.IntegerField(verbose_name='成员', default=0)


class TeamMember(models.Model):
    teammemberid = models.AutoField(primary_key=True)
    teamid = models.ForeignKey(Team, on_delete=models.CASCADE)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.IntegerField(default=0)  # 0 群员 1 管理 2 群主

    class Meta:
        db_table = 'TeamMember'  # 改变当前模型类对应的表名


class ChatMessage(models.Model):
    STATUS_CHOICES = [
        ('unread', '未读'),
        ('read', '已读'),
    ]
    messageid = models.AutoField(primary_key=True)
    teamid = models.ForeignKey(Team, on_delete=models.CASCADE)
    senderid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    mentioneduserid = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='mentioned_messages',
                                        default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unread')

    class Meta:
        ordering = ['-timestamp']
        db_table = 'ChatMessage'

    def mark_as_read(self):
        self.status = 'read'
        self.save()

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}"


class TeamToProject(models.Model):
    teamid = models.IntegerField(verbose_name='团队', default=0)
    projectid = models.IntegerField(verbose_name='项目', default=0)


class Project(models.Model):
    projectid = models.AutoField(primary_key=True)
    teamid = models.ForeignKey(Team, on_delete=models.CASCADE)
    projectname = models.CharField(max_length=255)
    creatorid = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField('创造时间', default=timezone.now)
    def to_dic(self):
        return {
            "projectid": self.projectid,
            "teamid": self.teamid.teamid,
            "projectname": self.projectname,
            "creatorid":self.creatorid.username,
            "created_time":self.created_time
        }

    class Meta:
        db_table = 'Project'  # 改变当前模型类对应的表名


class PrototypePage(models.Model):
    pageid = models.AutoField(primary_key=True)
    projectid = models.ForeignKey(Project, on_delete=models.CASCADE)
    pagename = models.CharField(max_length=255)
    pagesize = models.IntegerField()
    pagecontent = models.TextField()

    class Meta:
        db_table = 'PrototypePage'


class Document(models.Model):
    documentid = models.AutoField(primary_key=True)
    projectid = models.ForeignKey(Project, on_delete=models.CASCADE)
    documenttitle = models.CharField(max_length=255)
    documentcontent = models.TextField()

    class Meta:
        db_table = 'Document'


class Folder(models.Model):
    folderid = models.AutoField(primary_key=True)
    projectid = models.ForeignKey(Project, on_delete=models.CASCADE)
    foldertitle = models.CharField(max_length=255)
    documentid = models.ForeignKey(Document, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Folder'


class DocumentVersion(models.Model):
    versionid = models.AutoField(primary_key=True)
    documentid = models.ForeignKey(Document, on_delete=models.CASCADE)
    versioncontent = models.TextField()
    timestamp = models.DateTimeField()

    class Meta:
        db_table = 'DocumentVersion'


class PublicChat(models.Model):
    chatid = models.AutoField(primary_key=True)
    teamid = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        db_table = 'PublicChat'


class PublicChatMember(models.Model):
    chat_member_id = models.AutoField(primary_key=True)
    chatid = models.ForeignKey('PublicChat', on_delete=models.CASCADE)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'PublicChatMember'

    def __str__(self):
        return f"PublicChatMember {self.chat_member_id}"

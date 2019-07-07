from django import forms
from agency.models import Notice,Lessons

class UserForm(forms.Form):
    username=forms.CharField(min_length=4 ,max_length=20,label="用户名",widget=forms.TextInput())
    password = forms.CharField(min_length=8,label="密码",widget=forms.PasswordInput())

class UserAForm(forms.Form):
    GENDER_CHOICES = (
        ('M', '男'),
        ('F', '女'),
    )
    FIELD_CHOICES = (
        ('M','数学'),
        ('E','英语'),
        ('C','语文'),
        ('O','其他'),
    )
    AGE_CHOICE=(
        ('A','学前教育'),
        ('B','小学教育'),
        ('C','中学教育'),
        ('D','高中教育'),
    )
    username=forms.CharField(min_length=4,max_length=20,label="用户名",widget=forms.TextInput())
    password = forms.CharField(min_length=8,label="密码",widget=forms.PasswordInput())
    email = forms.EmailField(label="电子邮件",widget=forms.EmailInput())
    field = forms.ChoiceField(label="教育领域",choices=FIELD_CHOICES)    ##field varchar(100) not null,
    idcode = forms.CharField( label="标识码",max_length=30 )    ##idcode varchar(30) not null,
    address = forms.CharField( label="店面地址",max_length=100 )  ##address varchar(100) ,  
    aim_age = forms.ChoiceField(label="教育适合年龄",choices=AGE_CHOICE)
    phone = forms.CharField( label="联系电话",max_length=13 )
    intro = forms.CharField(label="简介",max_length=200)


class UserTForm(forms.Form):
    GENDER_CHOICES = (
        ('M', '男'),
        ('F', '女'),
    )
    AGE_CHOICE=(
        ('A','学前教育'),
        ('B','小学教育'),
        ('C','中学教育'),
        ('D','高中教育'),
    )
    FIELD_CHOICES = (
        ('M','数学'),
        ('E','英语'),
        ('C','语文'),
        ('O','其他'),
    )
    username=forms.CharField(min_length=4,max_length=13,label="用户名",widget=forms.TextInput())
    password = forms.CharField(min_length=8,label="密码",widget=forms.PasswordInput())
    name=forms.CharField(max_length=20,label="真实姓名")
    idcard = forms.CharField(label="身份证",max_length=18)
    email=forms.EmailField(label="电子邮件")
    field = forms.ChoiceField( label="教育领域",choices=FIELD_CHOICES )    ##field varchar(100) not null,  
    aim_age = forms.ChoiceField(label="教育适合年龄",choices=AGE_CHOICE)
    phone = forms.CharField( label="联系电话",max_length=13 )
    sex =forms.ChoiceField(label='性别',choices=GENDER_CHOICES)
    age =forms.IntegerField(label="年龄")    ##
    address = forms.CharField(label="地址",max_length=200)
    intro = forms.CharField(label="简介",max_length=200)



class NoticeForm(forms.Form):
    notice_title=forms.CharField(min_length=4,max_length=20,empty_value="请输入标题",label="标题",widget=forms.TextInput())
    notice_content=forms.CharField(min_length=8,max_length=200,empty_value="请输入内容",widget=forms.Textarea())

class NoticeAddForm(forms.ModelForm):
    notice_title = forms.CharField(min_length=4,max_length=30,
                               error_messages={
                                   'min_length': '标题不少于4个字符',
                                   'max_length': '标题不能多于30个字符',
                                   'required': '标题不能为空',
                               },
                               widget=forms.TextInput(attrs={'placeholder': '请输入标题'}))
    notice_content = forms.CharField(error_messages={'required': '不能为空',},
        widget=forms.Textarea(attrs = {'placeholder': '请输入评论内容' })
    )
    class Meta:
        model = Notice
        fields = ['notice_title', 'notice_content']

class LessonPublishForm(forms.ModelForm):
    AGE_CHOICE=(
        ('A','学前教育'),
        ('B','小学教育'),
        ('C','中学教育'),
        ('D','高中教育'),
    )
    FIELD_CHOICES = (
        ('M','数学'),
        ('E','英语'),
        ('C','语文'),
        ('O','其他'),
    )
    cname = forms.CharField(min_length=4, max_length=200, required=True,
                              error_messages={
                                  'min_length': '至少4个字符',
                                  'max_length': '不能多于200个字符',
                                  'required': '标题不能为空'
                              },
                              widget=forms.TextInput(attrs={'placeholder': '请输入内容'}))
    ccontend = forms.CharField(min_length=4, max_length=200, required=True,
                              error_messages={
                                  'min_length': '至少4个字符',
                                  'max_length': '不能多于200个字符',
                                  'required': '描述不能为空'
                              },
                              widget=forms.Textarea(attrs={'placeholder': '请输入内容'}))
    cstarttime = forms.DateField(widget=forms.DateInput(attrs={'class': 'date-pick','placeholder' : '开始时间(年/月/日)'},
                                        format='%m/%d/%Y'))
    cendtime = forms.DateField(widget=forms.DateInput(attrs={'class': 'date-pick','placeholder' : '结束时间(年/月/日)'},
                                        format='%m/%d/%Y'))
    cprice = forms.IntegerField(min_value=0)
    caim_age = forms.ChoiceField(choices=AGE_CHOICE)
    cfield = forms.ChoiceField( label="教育领域",choices=FIELD_CHOICES )    ##field varchar(100) not null,
    carea = forms.CharField(min_length=4,max_length=50)
    cteacher= forms.CharField(min_length=1,max_length=50)
    chomework=forms.CharField(min_length=1,max_length=50)
    lesson_user=forms.CharField(max_length=20,required=False)
    class Meta:
        model = Lessons
        fields = '__all__'


class ChangePriceForm(forms.Form):
    new_price = forms.IntegerField(min_value=0,error_messages={'required': '不能为空',})
    
        

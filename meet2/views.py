from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
# from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required


from . forms import *
from . models import *


def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST)
        phone_form = PhoneForm(request.POST)

        if form.is_valid() and profile_form.is_valid() and phone_form.is_valid():
            user = form.save()
            user.refresh_from_db()

            user.profile.AddressRoomNo = profile_form.cleaned_data.get('AddressRoomNo')
            user.profile.AddressHall = profile_form.cleaned_data.get('AddressHall')
            user.save()

            phone1 = PhoneNumber()
            phone1.UserId = user
            phone1.PhoneNumber = phone_form.cleaned_data.get('PhoneNumber1')
            phone1.save()

            check_phone = phone_form.cleaned_data.get('PhoneNumber2')

            if check_phone is not None:
                phone2= PhoneNumber()
                phone2.UserId = user
                phone2.PhoneNumber = check_phone
                phone2.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')   
        else:
            messages.error(request, "Invalid Form Details")     
    else:
        form = SignUpForm()
        profile_form = ProfileForm()
        phone_form = PhoneForm()
    return render(request, 'signup.html', {'form':form, 'profile_form':profile_form, 'phone_form':phone_form})        

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.error(request, "You are now logged in as {username}")
                return redirect('index')
            elif user.is_superuser is True:
                messages.error(request, "This is not for admin login")  
            else:
                messages.error(request, "Invaild username or password")
        else:
            messages.error(request, "Invalid username or password")
    form = AuthenticationForm()
    return render(request, "login.html", context={"form":form})

def logout_request(request):
    user = request.user
    if user.username:
        logout(request)
        messages.info(request, "Logged out successfully")
    else:
        messages.info(request, "You are already logged out")
    return redirect('home')

def index(request):
    user = request.user
    if user.username and user.is_superuser is False:
        PN = PhoneNumber.objects.filter(UserId=user)
        phone_nos = []

        for phone in PN:
            phone_nos.append(phone.PhoneNumber)
        
        return render(request, 'index.html', {'phone_nos':phone_nos})
    else:
        messages.warning(request, 'You are not logged in. Please login') 
        return redirect('home')  

def show_joined_group(request):
    user = request.user                                     

    if user.username and user.is_superuser is False:
        GM = GroupMembers.objects.filter(UserId=user)

        user_groups = []
        for x in GM:
            user_groups.append(x.GroupId)
        return render(request, 'show_group.html', {'user_groups':user_groups})
    else:
        messages.warning(request, 'You are not logged in. Please login') 
        return redirect('home')

def show_new_group(request):
    user = request.user

    if user.username and user.is_superuser is False:
        GM = GroupMembers.objects.filter(UserId=user)

        user_groups = []
        for x in GM:
            user_groups.append(x.GroupId)

        all_groups = Group.objects.all()

        new_groups = []

        for group in all_groups:
            if group not in user_groups:
                new_groups.append(group)       

        return render(request, 'new_group.html', {'new_groups':new_groups})
    else:
        messages.warning(request, 'You are not logged in. Please login') 
        return redirect('home')    

def join_group(request, id):
    user = request.user   
    if user.username and user.is_superuser is False:
        cur_group = Group.objects.get(GroupId = id)

        new_member = GroupMembers()
        new_member.GroupId = cur_group
        new_member.UserId = user
        new_member.save()


        return redirect(show_joined_group)
    else:
        messages.warning(request, 'You are not logged in. Please login')
        return redirect('home')    


def new_post(request, id):
    user = request.user 
    if user.username and user.is_superuser is False:
        GM = GroupMembers.objects.filter(GroupId = id, UserId = user)

        if GM is None:
            messages.error(request, "Not a member of group")
            return redirect('index')
        else:
            if request.method =="POST":
                form = PostForm(request.POST)
                
                if form.is_valid():
                    post = form.save(commit = False)
                    post.UserId = request.user
                    post.save()
                    pid = post.PostId
                    new_post_rel = HasPosts()
                    new_post_rel.GroupId = Group.objects.get(GroupId = id)
                    new_post_rel.PostId = Post.objects.get(PostId = pid)
                    new_post_rel.save()
                    return redirect(show_posts,id)
                else:
                    messages.error(request, "Invalid Form Details")
            else:
                form = PostForm()
            return render(request,'new_post.html',{'new_post_form':PostForm,'gid':id})
    else:
        messages.warning(request, 'You are not logged in. Please login')
        return redirect('home')    

def show_posts(request, id):
    user = request.user 
    if user.username and user.is_superuser is False:
        GM = GroupMembers.objects.filter(GroupId = id, UserId = user)
        print(GM)
        if GM is None:
            messages.error(request, "Not a member of group")
            return redirect('index')
        else:
            HP = HasPosts.objects.filter(GroupId = id)
            all_posts = Post.objects.all()
            
            has_post = []
            for x in all_posts:
                for y in HP:
                    if x.PostId == y.PostId.PostId :
                        has_post.append(x)
            
            moderator = []
            for z in GM:          
                moderator.append(z.Moderator)
              
            return render(request, 'group_posts.html',{'hps':has_post,'gid':id,'moderator':moderator})
    else:
        messages.warning(request, 'You are not logged in. Please login')
        return redirect('home')    

def new_comment(request,id):
    user = request.user 
    if user.username and user.is_superuser is False:
        if request.method == "POST":
            form = CommentForm(request.POST)
            
            if form.is_valid():
                comments = form.save(commit = False)
                comments.UserId = request.user
                comments.PostId = Post.objects.get(PostId = id)
                comments.save()
                return redirect(show_comments,id)
            else:
                messages.error(request, "Invalid Form Details")    
        else:
            form = CommentForm()
        return render(request,'new_comment.html',{'new_comment_form':CommentForm})
    else:
        messages.warning(request, 'You are not logged in. Please login')
        return redirect('home')    

def show_comments(request, id):
    user = request.user 
    if user.username and user.is_superuser is False:
        HC = Comments.objects.filter(PostId = id)
        print(HC)
        return render(request, 'post_comments.html',{'hcs':HC,'pid':id})
    else:
        messages.warning(request, 'You are not logged in. Please login')
        return redirect('home')


def add_event(request,id):
    user = request.user 
    if user.username and user.is_superuser is False:
        if request.method == "POST":
            form = EventForm(request.POST)
            if form.is_valid():
                events = form.save(commit = False)
                events.save()
                eid = events.EventId
                new_hasevents_rel = HasEvents()
                new_hasevents_rel.GroupId = Group.objects.get(GroupId = id)  #//id
                new_hasevents_rel.EventId = Events.objects.get(EventId = eid)
                new_hasevents_rel.save()
                return redirect(show_group_events,id)
            else :
                messages.error(request, "Invalid Form Details")
                return redirect('home')    

        else:
            form = EventForm()
        return render(request,'new_event.html',{'new_event_form':EventForm,'gid':id})
    else:
        messages.warning(request, 'You are not logged in. Please login')
        return redirect('home')

def show_group_events(request,id):
    user = request.user
    if user.username and user.is_superuser is False:
        GM = GroupMembers.objects.filter(GroupId = id, UserId = user)

        if GM is None:
            messages.error(request, "Not a member of group")
            return redirect('index')
        else:    
            UIE = UserInterestedEvents.objects.filter(UserId = user)
            all_group_event = []
            all_user_event = []
            group = Group.objects.get(GroupId = id)
            GE = HasEvents.objects.filter(GroupId = group)
            for x in GE:
                all_group_event.append(x.EventId)
            for y in UIE:
                all_user_event.append(y.EventId)
            joined_event = []
            not_joined_event = []
            for x in all_group_event :
                if x in all_user_event:
                    joined_event.append(x)
                else:
                    not_joined_event.append(x)
            return render(request,'show_group_event.html',{'joined':joined_event,'not_joined':not_joined_event,'gid':id})
    else:
        messages.warning(request, 'You are not logged in. Please login')
        return redirect('home')


def join_event(request, id):
    user = request.user
    if user.username and user.is_superuser is False:
        if request.method == "POST":
            form = UserInterestedEventsForm(request.POST)
            
            if form.is_valid():
                jevent = form.save(commit = False)
                jevent.UserId = user
                jevent.EventId = Events.objects.get(EventId = id)
                jevent.save()
                return redirect(show_all_events)
            else:
                messages.error(request, "Invalid Form Details")      
        else:
            form = UserInterestedEventsForm()
        return render(request,'join_event.html',{'join_event_form':UserInterestedEventsForm})
    else:
        messages.warning(request, 'You are not logged in. Please login')
        return redirect('home')


def show_all_events(request): #notification
    user = request.user
    if user.username and user.is_superuser is False:
        UIE = UserInterestedEvents.objects.filter(UserId = user)
        
        notifi = []
        for x in UIE:
            temp = []
            temp.append(x.EventId)
            temp.append(x.EntryTime)
            temp.append(x.ExitTime)
            notifi.append(temp)
            print(notifi)
        return render(request, 'show_all_event.html',{'notifi':notifi})
    else:
        messages.warning(request, 'You are not logged in. Please login')
        return redirect('home')


def mod_group_mem_all(request,id):
    user = request.user
    if user.username and user.is_superuser is False:
        group = Group.objects.get(GroupId = id)
        curr_user = GroupMembers.objects.get(UserId = user , GroupId = id)
        
        if not curr_user.Moderator :
            return redirect('home')
        
        group_user = GroupMembers.objects.filter(GroupId = group)
        GM = []
        for x in group_user:
            if x.UserId != user:
                GM.append(x.UserId)
        return render(request,'mod_show_members.html',{'group_mem':GM,'gid':id})
    else:
        messages.warning(request, 'You are not logged in. Please login')
        return redirect('home')



def mod_group_mem_del(request,gid,uid):
    user = request.user
    if user.username and user.is_superuser is False:
        GM = GroupMembers.objects.filter(GroupId = gid, UserId = user)

        if GM is None:
            messages.error(request, "Not a member of group")
            return redirect('index')
        else:    
            group = Group.objects.get(GroupId = gid)
            del_user = User.objects.get(id = uid)
            curr_user = GroupMembers.objects.get(UserId = user , GroupId = gid)
            if not curr_user.Moderator :
                messages.error(request, "You are not a moderator")
                return redirect('home')
            GroupMembers.objects.get(GroupId = group , UserId = del_user).delete()
            return redirect(mod_group_mem_all,gid)
    else:
        messages.warning(request, 'You are not logged in. Please login')
        return redirect('home')

def like_post(request, pid):
    user = request.user
    
    if user.username and user.is_superuser is False:
        cur_group = HasPosts.objects.get(PostId = pid)
        gid = cur_group.GroupId.GroupId
        cur_post = Post.objects.get(PostId = pid)
        cur_post.Likes = cur_post.Likes+1
        cur_post.save()
        return redirect('show_posts', gid)
    else:
        messages.warning(request, 'You are not logged in. Please login')
        return redirect('home')    

def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')  

            user = authenticate(username=username, password=password)

            if user is None:
                messages.error(request, "Invalid username or password")
            elif user.is_superuser is not True:
                messages.error(request, "This is for admin login")
            else:
                login(request, user)
                messages.error(request, "You are now logged in as {username}")
                return redirect('admin_show_groups')    
        else:
            messages.error(request, "Invalid username or password")
    form = AuthenticationForm()
    return render(request, "admin_login.html", context={"form":form})    

def admin_show_groups(request): 
    user = request.user
    if user.username and user.is_superuser is True:
        all_groups = Group.objects.all()
        return render(request, "admin_show_group.html", {'all_groups':all_groups})    
    else:
        messages.warning(request, 'Error in admin login')
        return redirect('home')

def admin_show_mems(request, gid):
    user = request.user
    if user.username and user.is_superuser is True:
        GM = GroupMembers.objects.filter(GroupId = gid)
        members = []

        for mems in GM:
            temp = []
            temp.append(mems.UserId)
            temp.append(gid)
            temp.append(mems.Moderator)
            members.append(temp)

        return render(request, "admin_show_mems.html", {'members':members}) 
    else:
        messages.warning(request, 'Error in admin login')
        return redirect('home')  

def admin_group_moderator(request, gid, uid, boolvalue):
    user = request.user
    if user.username and user.is_superuser is True:
        GM = GroupMembers.objects.get(GroupId=gid, UserId= uid)
        GM.Moderator = boolvalue
        GM.save()
        return redirect('admin_show_mems', gid)
    else:
        messages.warning(request, 'Error in admin login')
        return redirect('home')              
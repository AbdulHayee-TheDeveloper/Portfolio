"""
Django Admin Configuration for Portfolio Website
Experience model handles both Jobs and Skills
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Experience, Education, Project, Service, Contact


# ======================== EXPERIENCE ADMIN (Jobs + Skills) ========================

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = [
        'icon_preview',
        'title',
        'type_badge',
        'company_or_category',
        'proficiency_or_dates',
        'visibility_status',
        'order'
    ]
    list_filter = ['experience_type', 'visible', 'proficiency', 'ongoing', 'category']
    search_fields = ['title', 'company', 'description', 'category']
    list_editable = ['order']
    readonly_fields = ['created_at', 'updated_at', 'icon_display']
    list_per_page = 25
    
    actions = ['mark_as_visible', 'mark_as_hidden', 'convert_to_skill', 'convert_to_job']
    
    fieldsets = (
        ('Type Selection', {
            'fields': ('experience_type',),
            'description': 'Select whether this is a Job Experience or Technical Skill'
        }),
        ('Basic Information', {
            'fields': ('title', 'description', 'icon', 'icon_display')
        }),
        ('Job Experience Fields', {
            'fields': ('company', 'location', 'start_date', 'end_date', 'ongoing'),
            'classes': ('collapse',),
            'description': 'Fill these only for Job Experiences'
        }),
        ('Skill Fields', {
            'fields': ('proficiency', 'category'),
            'classes': ('collapse',),
            'description': 'Fill these only for Technical Skills'
        }),
        ('Display Settings', {
            'fields': ('visible', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def icon_preview(self, obj):
        """Show icon/logo in list view"""
        if obj.icon:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius: 6px; object-fit: cover; border: 1px solid #ddd;" />',
                obj.icon.url
            )
        emoji = '💼' if obj.experience_type == 'job' else '💡'
        return format_html(
            '<div style="width:40px;height:40px;background:#f0f0f0;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:1.5rem;">{}</div>',
            emoji
        )
    icon_preview.short_description = 'Icon'
    
    def icon_display(self, obj):
        """Large icon preview in detail view"""
        if obj.icon:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px; border-radius: 12px; border: 2px solid #4fffb0;" />',
                obj.icon.url
            )
        return "No icon uploaded"
    icon_display.short_description = 'Current Icon'
    
    def type_badge(self, obj):
        """Show type badge with colors"""
        if obj.experience_type == 'job':
            return format_html(
                '<span style="background: #00d4ff; color: #000; padding: 4px 12px; border-radius: 12px; font-weight: 600; font-size: 11px;">JOB</span>'
            )
        return format_html(
            '<span style="background: #4fffb0; color: #000; padding: 4px 12px; border-radius: 12px; font-weight: 600; font-size: 11px;">SKILL</span>'
        )
    type_badge.short_description = 'Type'
    
    def company_or_category(self, obj):
        """Show company for jobs or category for skills"""
        if obj.experience_type == 'job':
            return obj.company or '-'
        return obj.category or '-'
    company_or_category.short_description = 'Company/Category'
    
    def proficiency_or_dates(self, obj):
        """Show proficiency for skills or dates for jobs"""
        if obj.experience_type == 'skill':
            colors = {
                'Beginner': '#ffa500',
                'Intermediate': '#4fffb0',
                'Advanced': '#00d4ff',
                'Expert': '#ff69b4',
            }
            color = colors.get(obj.proficiency, '#4fffb0')
            return format_html(
                '<span style="background: {}; color: #000; padding: 4px 12px; border-radius: 12px; font-weight: 600; font-size: 11px;">{}</span>',
                color,
                obj.proficiency
            )
        if obj.start_date:
            end = 'Present' if obj.ongoing else (obj.end_date.strftime('%Y') if obj.end_date else '-')
            return f"{obj.start_date.strftime('%Y')} - {end}"
        return '-'
    proficiency_or_dates.short_description = 'Level/Duration'
    
    def visibility_status(self, obj):
        """Show visibility status"""
        if obj.visible:
            return format_html('<span style="color: green; font-weight: bold;">✓ Visible</span>')
        return format_html('<span style="color: red; font-weight: bold;">✗ Hidden</span>')
    visibility_status.short_description = 'Status'
    
    # Custom Actions
    def mark_as_visible(self, request, queryset):
        updated = queryset.update(visible=True)
        self.message_user(request, f'{updated} item(s) marked as visible.')
    mark_as_visible.short_description = 'Mark selected as visible'
    
    def mark_as_hidden(self, request, queryset):
        updated = queryset.update(visible=False)
        self.message_user(request, f'{updated} item(s) hidden from website.')
    mark_as_hidden.short_description = 'Hide selected items'
    
    def convert_to_skill(self, request, queryset):
        updated = queryset.update(experience_type='skill')
        self.message_user(request, f'{updated} item(s) converted to Skills.')
    convert_to_skill.short_description = 'Convert to Technical Skill'
    
    def convert_to_job(self, request, queryset):
        updated = queryset.update(experience_type='job')
        self.message_user(request, f'{updated} item(s) converted to Job Experience.')
    convert_to_job.short_description = 'Convert to Job Experience'


# ======================== EDUCATION ADMIN ========================

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['title', 'institution', 'degree_level', 'start_date', 'end_date', 'ongoing', 'visible', 'order']
    list_editable = ['visible', 'order', 'ongoing']
    list_filter = ['degree_level', 'ongoing', 'visible', 'institution']
    search_fields = ['title', 'institution', 'location', 'summary']
    date_hierarchy = 'start_date'
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['order', '-start_date']

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'institution', 'logo', 'location')
        }),
        ('Timing', {
            'fields': ('start_date', 'end_date', 'ongoing')
        }),
        ('Details', {
            'fields': ('degree_level', 'grade_or_gpa', 'summary')
        }),
        ('Display Settings', {
            'fields': ('visible', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# ======================== PROJECT ADMIN ========================

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'is_featured', 'order', 'created_at']
    list_filter = ['status', 'is_featured', 'created_at']
    search_fields = ['title', 'description', 'tech_stack']
    list_editable = ['is_featured', 'order']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-order', '-created_at']
    list_per_page = 20
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'status')
        }),
        ('Media & Links', {
            'fields': ('path', 'demo', 'github')
        }),
        ('Technologies', {
            'fields': ('tech_stack',),
            'description': 'Technologies ko comma-separated enter karein'
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# ======================== SERVICE ADMIN ========================

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'duration', 'visible', 'order', 'created_at']
    list_filter = ['category', 'visible', 'created_at']
    search_fields = ['title', 'description', 'short_description']
    list_editable = ['visible', 'order']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['order', 'title']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'short_description', 'icon')
        }),
        ('Details', {
            'fields': ('description', 'details', 'category', 'duration')
        }),
        ('Media & Links', {
            'fields': ('image', 'link')
        }),
        ('Display Settings', {
            'fields': ('visible', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# ======================== CONTACT ADMIN ========================

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'short_message', 'created_date', 'read_status', 'reply_status']
    list_filter = ['is_read', 'replied', 'created_at']
    search_fields = ['name', 'email', 'phone', 'message']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 25
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    actions = ['mark_as_read', 'mark_as_unread', 'mark_as_replied']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Status', {
            'fields': ('is_read', 'replied')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def short_message(self, obj):
        return obj.get_short_message()
    short_message.short_description = 'Message Preview'
    
    def created_date(self, obj):
        return obj.created_at.strftime("%d %b %Y, %I:%M %p")
    created_date.short_description = 'Received On'
    created_date.admin_order_field = 'created_at'
    
    def read_status(self, obj):
        if obj.is_read:
            return format_html('<span style="color: green; font-weight: bold;">✓ Read</span>')
        return format_html('<span style="color: orange; font-weight: bold;">✉ Unread</span>')
    read_status.short_description = 'Status'
    
    def reply_status(self, obj):
        if obj.replied:
            return format_html('<span style="color: blue; font-weight: bold;">✓ Replied</span>')
        return format_html('<span style="color: gray;">- Not Replied</span>')
    reply_status.short_description = 'Reply'
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} message(s) marked as read.')
    mark_as_read.short_description = 'Mark selected as read'
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} message(s) marked as unread.')
    mark_as_unread.short_description = 'Mark selected as unread'
    
    def mark_as_replied(self, request, queryset):
        updated = queryset.update(replied=True)
        self.message_user(request, f'{updated} message(s) marked as replied.')
    mark_as_replied.short_description = 'Mark selected as replied'

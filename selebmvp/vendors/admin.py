from django.contrib import admin
from .models import (Vendor, LocationAmenity, CateringAmenity,
                     VendorSocialReview, VendorAddress, VendorPhoto,
                     VendorLocationService, VendorCateringService,
                     VendorServicePhoto)
# from django import forms
# from functools import partial

admin.site.register(LocationAmenity)
admin.site.register(CateringAmenity)


class VendorSocialReviewInLine(admin.TabularInline):
    model = VendorSocialReview
    extra = 1


class VendorAddressInLine(admin.StackedInline):
    model = VendorAddress


class VendorPhotoInLine(admin.TabularInline):
    model = VendorPhoto
    extra = 1


# class VendorLocationServiceInLineForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(VendorLocationServiceInLineForm, self).__init__(*args, **kwargs)
#         self.fields['photos'].queryset = VendorPhoto.objects.filter(
#             vendor=self.instance)


class VendorLocationServiceInLine(admin.StackedInline):
    model = VendorLocationService
    extra = 1

    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     if db_field.name == "photos":
    #         kwargs["queryset"] = VendorPhoto.objects.filter(
    #                 vendor=request.GET.id)
    #     return super(VendorLocationServiceInLine,
    #                  self).formfield_for_manytomany(db_field,
    #                                                 request,
    #                                                 **kwargs)

        # def get_formset(self, request, obj=None, **kwargs):
        #     kwargs['formfield_callback'] = partial(self.formfield_for_dbfield,
        #                                            request=request, obj=obj)
        #     return super(VendorLocationServiceInLine, self).get_formset(
        # request,
        #                                                                 obj,
        #
        # **kwargs)
        #
        # def formfield_for_dbfield(self, db_field, **kwargs):
        #     vendor = kwargs.pop('obj', None)
        #     formfield = super(VendorLocationServiceInLine,
        #                       self).formfield_for_dbfield(db_field, **kwargs)
        #     if db_field.name == "photos" and vendor:
        #         kwargs["queryset"] = VendorPhoto.objects.filter(
        #                 vendor=vendor)
        #     return formfield


class VendorCateringServiceInLine(admin.StackedInline):
    model = VendorCateringService
    extra = 1

    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     if db_field.name == "photos":
    #         kwargs["queryset"] = VendorPhoto.objects.filter(
    #                 vendor=request.GET.get('id'))
    #     return super(VendorCateringServiceInLine,
    #                  self).formfield_for_manytomany(db_field,
    #                                                 request,
    #                                                 **kwargs)


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    inlines = [
        VendorAddressInLine,
        VendorSocialReviewInLine,
        VendorPhotoInLine,
        VendorLocationServiceInLine,
        VendorCateringServiceInLine
    ]

admin.site.register(VendorServicePhoto)
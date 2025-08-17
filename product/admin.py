from django.contrib import admin

# Register your models here.

from .models import AttrbiuteProduct, Product, ProductImage, ProdctColler

class AttributeInline(admin.TabularInline):
    list_display = ['product__title','name','value']
    model = AttrbiuteProduct
    extra = 2

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductCollerInline(admin.TabularInline):
    model = ProdctColler
    extra = 1

class ProudctAdmin(admin.ModelAdmin):
    list_display = ["title"]
    inlines = [AttributeInline,ProductImageInline,ProductCollerInline]
    exclude = ['final_price']



admin.site.register(Product,ProudctAdmin)

admin.site.register(ProductImage)
admin.site.register(AttrbiuteProduct)
admin.site.register(ProdctColler)


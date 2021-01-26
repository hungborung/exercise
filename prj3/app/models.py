import itertools

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from django.core.files import File
from io import BytesIO
from PIL import Image
# Create your models here.

class CategoryMixin(object):
    name = models.CharField(max_length=settings.APP_UNIQUE_SLUG_MAX_LENGTH)

class Category(CategoryMixin,models.Model):
    code = models.CharField(max_length=30, verbose_name='Mã', unique=True)
    name = models.CharField(max_length=settings.APP_UNIQUE_SLUG_MAX_LENGTH, verbose_name='Tên')
    slug = models.SlugField( default='',editable=False,max_length=settings.APP_UNIQUE_SLUG_MAX_LENGTH,)
    cat_parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def get_absolute_url(self):
        kwargs = {"slug": self.slug}
        return reverse("categoryunique-slug", kwargs=kwargs)

    def _generate_slug(self):
        max_length = settings.APP_UNIQUE_SLUG_MAX_LENGTH
        value = self.name
        slug_candidate = slug_original = slugify(value, allow_unicode=True)[:max_length]
        for i in itertools.count(1):
            if not Category.objects.filter(slug=slug_candidate).exists():
                break
            # Calculate the length of the candidate slug
            # considering separator and number length
            id_length = len(str(i)) + 1
            new_slug_text_part_length = len(slug_original) - id_length
            original_slug_with_id_length = len(slug_original) + id_length
            # truncate the candidate slug text if the whole candidate slug length
            # is greater than the Slug's database max_length
            candidate_slug_part = slug_original[:new_slug_text_part_length] if original_slug_with_id_length > max_length else slug_original
            slug_candidate = "{}-{}".format(candidate_slug_part, i)

        self.slug = slug_candidate

    def slug_length(self):
        return len(self.slug)

    def get_absolute_url(self):
        # if self.cat_parent:
        #     return '/%s/%s' % (self.cat_parent.slug) % (self.slug)  
        # else:
            return '/%s/' % (self.slug)
            
    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()

        super().save(*args, **kwargs)

    class Meta:
        #enforcing that there can not be two categories under a parent with same slug
        
        # __str__ method elaborated later in post.  use __unicode__ in place of
        
        # __str__ if you are using python 2

        unique_together = ('slug', 'cat_parent',)    
        verbose_name_plural = "categories"     

    def __str__(self):                           
        full_path = [self.name]                  
        k = self.cat_parent
        while k is not None:
            full_path.append(k.name)
            k = k.cat_parent
        return ' -> '.join(full_path[::-1])


class Publisher(models.Model):
    code = models.CharField(max_length=30, verbose_name='Mã', unique=True)
    name = models.CharField(max_length=255, verbose_name='Tên')
    slug = models.SlugField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    code = models.CharField(max_length=30, verbose_name='Mã', unique=True)
    name = models.CharField(max_length=255, verbose_name='Tên')
    slug = models.SlugField(max_length=255)
    publisher = models.ForeignKey(Publisher, verbose_name='Nhà xuất bản', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(verbose_name='Mô tả', blank=True, null=True)
    price_import = models.FloatField(verbose_name='Gias nhập')
    price_sell = models.FloatField(verbose_name='Giá bán')
    discount = models.FloatField(verbose_name='Giảm giá', null=True, blank=True, default=0)
    category = models.ForeignKey(Category, verbose_name='Nhóm', on_delete=models.PROTECT)  
    qty = models.FloatField(verbose_name='Số lượng')
    image = models.ImageField(blank=True,null=True ,upload_to='')
    is_featured = models.BooleanField(default=False)
    date_create = models.DateTimeField(verbose_name='Ngày tạo', auto_now_add=True )
    date_update = models.DateTimeField(verbose_name='Ngày sửa', null=True, auto_now=True)


    class Meta:
        ordering = ('-date_create',)
    def __str__(self):
        return self.name

   

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            if self.image:
                self.image = self.make_image(self.image)
                self.save()
                
                return self.image.url
            else:
                return ''
                
    def make_image(self, image, size=(300,200)):
        img = Image.open(image)
        img.convert('RGB')
        img.image(size)
        img_io = BytesIO()
        img.save(img_io, 'JPEG', quality=85)

        image = File(img_io, name = image.name)
        return image
    
    @property
    def price_discount(self):
        return self.price_sell * ((100-self.discount)/100)

class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='')

    def __str__(self):
        return self.title





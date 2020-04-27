from django.db import models

from location.models import Locate
from members.models import User

from core.models import TimeStampedModel as CoreModel

POST_CHOICES = (
    # 디지털/가전
    ('digital', '디지털/가전'),
    # 가구/인테리어
    ('furniture', '가구/인테리어'),
    # 유아동/유아도서
    ('baby', '유아동/유아도서'),
    # 생활/가공식품
    ('life', '생활/가공식품'),
    # 여성의류
    ('woman_wear', '여성의류'),
    # 여성잡화
    ('woman_goods', '여성잡화'),
    # 뷰티/미용
    ('beauty', '뷰티/미용'),
    # 남성패션/잡화
    ('male', '남성패션/잡화'),
    # 스포츠/레저
    ('sports', '스포츠/레저'),
    # 게임/취미
    ('game', '게임/취미'),
    # 도서/티켓/음반
    ('book', '도서/티켓/음반'),
    # 반려동물용품
    ('pet', '반려동물용품'),
    # 기타 중고물품
    ('other', '기타 중고물품'),
    # 삽니다
    ('buy', '삽니다'),

)
STATE_CHOICES = (
    # 판매중
    ('sales', '판매중'),
    # 예약중
    ('reserve', '예약중'),
    # 거래완료
    ('end', '거래완료'),
)


class Post(CoreModel):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text='작성자')
    title = models.CharField(
        max_length=100, help_text='제목')
    content = models.TextField(
        help_text='본문')
    address = models.CharField(
        max_length=200, help_text='대표 거래 지역')
    category = models.CharField(
        choices=POST_CHOICES, max_length=20, help_text='카테고리')
    price = models.IntegerField(
        default=0, help_text='가격')
    showed_locates = models.ManyToManyField(
        Locate, related_name='posts', blank=True, help_text='보여질 지역')
    view_count = models.IntegerField(
        default=0, help_text='조회 수')
    state = models.CharField(
        choices=STATE_CHOICES, max_length=10, default='sales', help_text='주문 상태')
    like_users = models.ManyToManyField(
        User, through='PostLike', related_name='like_post_set', blank=True, help_text='관심 유저'
    )

    class Meta:
        verbose_name = '게시글'
        verbose_name_plural = '%s 목록' % verbose_name

    @property
    def username(self):
        return self.author.username

    def __str__(self):
        return '{author} | {title} | {created}'.format(
            author=self.author.username,
            title=self.title,
            created=self.created,
        )


def post_image_path(instance, filename):
    return '/'.join(['post_images/', f'/post_{instance.post.id}/', filename])


# 사품 이미지
class PostImage(models.Model):
    photo = models.ImageField(
        upload_to=post_image_path, blank=True, help_text='상품 사진')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='post_images', help_text='게시글 번호')

    class Meta:
        verbose_name = '이미지'
        verbose_name_plural = '%s 목록' % verbose_name

    def __str__(self):
        return self.photo.url


# 관심
class PostLike(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, help_text='게시글 번호')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text='좋아요 누른 유저')

    class Meta:
        verbose_name = '관심'
        verbose_name_plural = '%s 목록' % verbose_name

    def __str__(self):
        return f'{self.author.username}가 {self.post.title} 을 좋아합니다.'


# 검색어
class SearchedWord(CoreModel):
    user = models.ForeignKey(
        User, related_name='searched_words', blank=True, null=True, on_delete=models.CASCADE)
    content = models.CharField(
        max_length=100, help_text='추천 검색어')
    count = models.IntegerField(
        default=0, help_text='검색 횟수')

    class Meta:
        verbose_name = '검색어'
        verbose_name_plural = '%s 목록' % verbose_name

    def __str__(self):
        return f'"{self.content}"가 {self.count}번 검색되었습니다.'


'''
# 리뷰
class PostReview(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = '리뷰'
        verbose_name_plural = '%s 목록' % verbose_name
'''

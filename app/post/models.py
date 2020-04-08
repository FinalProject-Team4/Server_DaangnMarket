
from django.db import models

from location.models import Locate
from members.models import User

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


class Post(models.Model):
    # 작성자
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 제목
    title = models.CharField(max_length=100)
    # 본문
    content = models.TextField()
    category = models.CharField(choices=POST_CHOICES, max_length=20)
    price = models.IntegerField(default=0)
    # 거래지역
    locate = models.ForeignKey(Locate, on_delete=models.CASCADE)
    # 보여질 지역
    showed_locate = models.ManyToManyField(Locate, related_name='showed_locate')
    view_count = models.IntegerField(default=0)
    # 상태
    state = models.CharField(choices=STATE_CHOICES, max_length=10, default='sales')

    updated = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '게시글'
        verbose_name_plural = '%s 목록' % verbose_name

    def __str__(self):
        return '{author} | {title} | {created}'.format(
            author=self.author.username,
            title=self.title,
            created=self.created,
        )


class PostImage(models.Model):
    photo = models.ImageField(upload_to='images/')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_images')

    class Meta:
        verbose_name = '이미지'
        verbose_name_plural = '%s 목록' % verbose_name

    def __str__(self):
        return self.photo.name


# 관심
class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = '관심'
        verbose_name_plural = '%s 목록' % verbose_name

    def __str__(self):
        return f'{self.user.id}가 {self.post.name} 을 좋아합니다.'


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


# 검색어
class RecommendWord(models.Model):
    content = models.CharField(max_length=100)
    count = models.IntegerField(default=0)

    class Meta:
        verbose_name = '추천 검색어'
        verbose_name_plural = '%s 목록' % verbose_name

    def __str__(self):
        return f'{self.content} 가 {self.count}번 검색되었습니다.'



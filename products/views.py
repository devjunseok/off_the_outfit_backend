import pandas as pd

from products.serializers import ProductSerializer, BrandSerializer, CategorySerializer, PostSerializer, ReplySerializer, ClosetSerializer, NameTagSerializer, NameTagViewSerializer, ClosetUserSerializer, ProductDetailSerializer
from products.models import Brand, Category, Product, Post, Reply, Closet, NameTag
from products.crawling import ProductsUpdate, MusinsaNumberProductsCreate

from communities.models import SearchWord

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status, permissions, filters, generics
from rest_framework_simplejwt.authentication import JWTAuthentication



# Products :: 상품 정보 관련 View 
class ProductInfoUdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # 무신사 상품 정보 업데이트 (Crawling)
    def post(self, request): 
        category_list = Category.objects.all().values()
        brand_list = Brand.objects.all().values()
        ProductsUpdate(category_list, brand_list)
        return Response({"message":"상품 정보가 업데이트 되었습니다!"}, status=status.HTTP_200_OK)
    

# 상품 정보 CRUD View          
class ProductInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # 상품 정보 전체 조회
    def get(self, request): 
        articles = Product.objects.all()
        serializer = ProductSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 상품 정보 개별 등록
    def post(self, request):         
        result = MusinsaNumberProductsCreate(request.data)
        
        if result == None:
            return Response({"message":"상품이 등록되었습니다!"}, status=status.HTTP_200_OK)
        
        elif result == "ERROR_01":
            return Response({"message":"이미 등록된 상품입니다.!"}, status=status.HTTP_200_OK)
        
        else:
            return Response({"message":"상품 등록에 실패했습니다."}, status=status.HTTP_200_OK)

# 상품정보 카테고리 별 조회 View
class ProductInfoCategoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request, category_id):
        articles = Product.objects.filter(category=category_id)
        serializer = ProductSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 상품정보 브랜드 별 조회 View
class ProductInfoBrandView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request, brand_id): 
        articles = Product.objects.filter(brand=brand_id)
        serializer = ProductSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 상품정보 카테고리 별 조회 View
class ProductInfoBrandiew(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request, category_id):
        articles = Product.objects.filter(category=category_id)
        serializer = ProductSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 상품 정보 상세 조회 View
class ProductInfoDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request, product_number): 
        product = get_object_or_404(Product, product_number=product_number)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 상품정보 게시글 View
class ProductPostView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # 상품 정보 게시글 전체 조회
    def get(self, request, product_number): 
        articles = Post.objects.filter(product__product_number=product_number)
        serializer = PostSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 상품 정보 게시글 작성
    def post(self, request, product_number): 
        product = Product.objects.get(product_number=product_number)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, product_id=product.id)
            return Response({"message":f"{serializer.data['post_type']}가 등록되었습니다!"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# 상품정보 게시글 상세 View
class ProductPostDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
     # 상품 정보 게시글 상세 조회
    def get(self, request, product_number, post_id):
        articles = Post.objects.filter(id=post_id, product__product_number=product_number)
        serializer = PostSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 상품 정보 게시글 수정
    def put(self, request):
        pass
    
    # 상품 정보 게시글 삭제
    def delete(self, request, product_number, post_id): 
        post = get_object_or_404(Post, id= post_id)
        if request.user == post.user:
            post.delete()
            return Response({"message":"게시글을 삭제했습니다!"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message":"권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN) 


# 상품 정보 게시글 댓글 View
class ProductPostReplyView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # 상품 정보 게시글 댓글 전체 조회
    def get(self, request): 
        pass
    
    # 상품 정보 게시글 댓글 등록
    def post(self, request, product_number, post_id): 
        product = Product.objects.get(product_number=product_number)
        serializer = ReplySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post_id=post_id)
            return Response({"message":"댓글이 등록되었습니다!"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# 상품 정보 게시글 댓글 상세 V
class ProductPostReplyDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # 상품 정보 게시글 댓글 삭제
    def delete(self, request, product_number, post_id, reply_id): 
        reply = get_object_or_404(Reply, id= reply_id)
        if request.user == reply.user:
            reply.delete()
            return Response({"message":"댓글을 삭제했습니다!"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message":"권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN)         



# Brand :: 브랜드 정보 관련 View 
class BrandInfoUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # 브랜드 정보 업데이트 (CSV)
    def post(self, request): 
        data = pd.read_csv('products/csv/brand_info.csv')

        for br in data['info']:
            brand = Brand()
            br_kr, br_en, br_link = br.split('|')
            
            # 중복 체크
            try : # 중복 브랜드
                brand_double_check = Brand.objects.get(brand_link=br_link)
            except : # 신규 브랜드
                brand_double_check = None
            
            if brand_double_check == None:
                brand.brand_name_kr = br_kr
                brand.brand_name_en = br_en
                brand.brand_link = br_link
                brand.save()
        
        return Response({"message":"브랜드 정보가 업데이트 되었습니다!"}, status=status.HTTP_200_OK)
    
# 상품 브랜드 정보 View
class BrandInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # 브랜드 정보 전체 조회
    def get(self, request): 
        articles = Brand.objects.all()
        serializer = BrandSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 브랜드 정보 개별 등록
    def post(self, request): 
        pass


# Category :: 카테고리 정보 관련 View     
class CategoryInfoUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # 카테고리 정보 업데이트 (CSV)
    def post(self, request):
        data = pd.read_csv('products/csv/category_info.csv')
        
        for cate in data['info']:
            category = Category()
            main_number, main_kr, main_en, sub_number, sub_kr, link = cate.split('|')
            
            # 중복 체크
            try : # 중복 카테고리
                category_double_check = Category.objects.get(category_link=link)
            except : # 신규 카테고리
                category_double_check = None
            
            if category_double_check == None:
                category.main_category_number = main_number
                category.main_category_name = main_kr
                category.sub_category_number = sub_number
                category.sub_category_name = sub_kr
                category.category_link = link
                category.save()
        
        return Response({"message":"카테고리 정보가 업데이트 되었습니다!"}, status=status.HTTP_200_OK)

# 카테고리 정보 View
class CategoryInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # 카테고리 정보 전체 조회
    def get(self, request): 
        articles = Category.objects.all()
        serializer = CategorySerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# Closet :: 옷장 관련 View
class ClosetView(APIView): 
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # 상품 기준 옷장 조회
    def get(self, request, product_number): 
        articles = Closet.objects.all().order_by('-created_at')
        serializer = ClosetSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 옷장 상품 등록 (name_tag 유무에 따라 등록)
    def post(self, request, product_number): 
        product = Product.objects.get(product_number=product_number)
        try:
            name_tag = request.data['name_tag']
        except:
            name_tag = None
        
        if name_tag == None:
            serializer = ClosetSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user, product_id=product.id)
                return Response({"message":"옷장에 상품이 등록되었습니다!"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            nametag = NameTag.objects.filter(tag_name=name_tag)
            name_tag_id = nametag.values()[0]['id']
            data = {
                "name_tag":name_tag_id
            }
            serializer = ClosetSerializer(data=data)
            if serializer.is_valid():
                serializer.save(user=request.user, product_id=product.id, name_tag_id=name_tag_id)
                return Response({"message":f"{name_tag} 옷장에 상품이 등록되었습니다!"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    
#옷장 상세보기 View
class ClosetDetailView(APIView): 
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # 옷장 수정
    def put(self, request, product_number, closet_id):
        try:
            name_tag = request.data['name_tag']
        except:
            name_tag = None
        if name_tag == None:
            data = {
                'name_tag': None
            }
        else:
            nametag = request.data['name_tag']
            name_tag = NameTag.objects.filter(tag_name = nametag)
            name_tag_id = name_tag.values()[0]['id']
            data = {
                'name_tag': name_tag_id
            }
        closet = get_object_or_404(Closet, id= closet_id)
        if request.user == closet.user:
            serializer = ClosetSerializer(closet, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"수정되었습니다!"}, status=status.HTTP_200_OK)

            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN)
    
    # 옷장 삭제
    def delete(self, request, product_number, closet_id):
        closet = get_object_or_404(Closet, id= closet_id)
        if request.user == closet.user:
            closet.delete()
            return Response({"message":"삭제했습니다!"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message":"권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN)         

    
# 옷장 삭제 View
class NameTagLikeView(APIView): 
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
     # 옷장 태그 좋아요
    def post(self, request, nametag_id ): 
        nametag = get_object_or_404(NameTag, id=nametag_id)
        if request.user in nametag.like.all():
            nametag.like.remove(request.user)
            return Response({"message":" 옷장 좋아요 취소 했습니다!"}, status=status.HTTP_200_OK)
        else:
            nametag.like.add(request.user)
            return Response({"message":"옷장 좋아요 했습니다!"}, status=status.HTTP_200_OK)
    
# 옷장 네임태그 View
class NameTagView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request):
        articles = NameTag.objects.filter(user_id=request.user.id)
        serializer = NameTagViewSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = NameTagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message":"옷장 태그가 등록되었습니다!"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 옷장 네임태그 상세조회 View
class NameTagDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request, nametag_id):
        articles = NameTag.objects.filter(user_id=request.user.id)
        serializer = NameTagViewSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# 옷장 View
class UserClosetView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request, user_id):
        articles = Closet.objects.filter(user_id=user_id)
        serializer = ClosetUserSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

# 상품 정보 검색 View
class ProductsSearchView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer # 게시글 전체 보기

    filter_backends = [filters.SearchFilter]

    search_fields = ['brand__brand_name_kr', 'brand__brand_name_en', 'product_number', 'product_name', 'category__main_category_name', 'category__sub_category_name']
    
    # 검색어 저장 추가
    def get(self, request, *args, **kwargs): 
        search = SearchWord()
        word = request.GET.get('search')
        search.word = word
        search.save()
        return self.list(request, *args, **kwargs)
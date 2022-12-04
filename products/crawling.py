import math
import sys, os
from bs4 import BeautifulSoup
import requests
from products.models import Products, Brand, Category


headers = os.environ.get("USER_AGENT")


def ProductsUpdate(Category_list, brand_list):
    for cate in Category_list[0:1]:
        urls = cate['category_link']
        category_id = Category.objects.filter(id=cate['id']) 
        sub_category_name = cate['sub_category_name']
        print(sub_category_name)
        
        # 브랜드 페이지_페이지네이션 최대 페이지 확인
        page_res = requests.get(urls, headers)
        page_res.raise_for_status()
        page_soup = BeautifulSoup(page_res.text, 'lxml')
        page_result = page_soup.find("span", attrs={"class":"totalPagingNum"}).get_text() # 최대 페이지
        # print(page_result)

        category_number = urls[len(urls)-6:]      # 카테고리 번호
        page_number = 5                           # 페이지 수 선택
        if int(page_result) < int(page_number):
            page_number = page_result
        for page in range(1, page_number):        # 1 ~ 최대 페이지까지 상품 정보 가져오기
            url = f"{urls}?d_cat_cd={category_number}&brand=&list_kind=small&sort=pop_category&sub_sort=&page={page}&display_cnt=90&group_sale=&exclusive_yn=&sale_goods=&timesale_yn=&ex_soldout=&kids=&color=&price1=&price2=&shoeSizeOption=&tags=&campaign_id=&includeKeywords=&measure="
            res = requests.get(url, headers)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'lxml')
            
            products_list_box = soup.find("ul", attrs={"id":"searchList"})
            # 각 페이지에서 상품 정보가져오기
            all_products = products_list_box.find_all("li", attrs={"class":"li_box"})
            for item in all_products:
                
                item_number = item["data-no"]
                try:
                    product_double_check = Products.objects.get(product_number=item_number)
                    print(f"{item_number} = 중복 상품")
                    pass
                except:
                    product_double_check = None
                    print(f"{item_number} = 신규 상품")
                
                if product_double_check == None: # 신규 상품 처리
                
                    # 브랜드명
                    brand_name = item.find("p", attrs={"class":"item_title"}).a
                    if brand_name != None:
                        brand_name = brand_name.get_text()
                    else:
                        pass
                    # print(brand_name)
                    for br in brand_list:
                        # print(br)
                        if brand_name == br['brand_name_kr']:
                            
                            # 상품 번호
                            product_number = item["data-no"]
                            print(product_number)
                            
                            # 상품 이미지
                            product_image = item.find("img", attrs={"class":"lazyload"})["data-original"]
                            # print(f"https:{product_image}")
                            
                            # 상품명
                            product_name = item.find("p", attrs={"class":"list_info"}).a.get_text()
                            product_name = product_name.replace(" ", "")
                            product_name = product_name.replace("\n", "")
                            
                            # 가격 (정상가/할인가)
                            price = item.find("p", attrs={"class":"price"}).get_text()
                            price = price.replace(",", "").replace("원", "").split()
                            if len(price) == 2:
                                original_price = price[0]
                                discount_price = price[1]
                            else:
                                original_price = price[0]
                                discount_price = price[0]

                            # 리뷰 갯수
                            review_count = item.find("span", attrs={"class":"count"})
                            if review_count != None:
                                review_count = int(review_count.get_text().replace(",", ""))
                            else:
                                review_count = 0
                                
                            # 브랜드 정보
                            brand_id = Brand.objects.get(id=br['id']) 
                            # print(f"{brand_id} / {product_name} / {discount_rate} / {category_id} / {original_price} / {review_count}")
                            
                            instance = Products.objects.create(
                                brand = brand_id,
                                product_number = product_number,
                                product_name = product_name,
                                product_image = f"https:{product_image}",
                                original_price = int(original_price),
                                discount_price = int(discount_price),
                                review_count = int(review_count)
                            )
                            instance.category.set(category_id)
                        else:
                            pass


def MusinsaNumberProductsCreate():
    pass
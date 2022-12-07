import os
from bs4 import BeautifulSoup
import requests
from products.models import Product, Brand, Category


headers = {"User-Agent":os.environ.get("USER_AGENT")}

# 상품 정보 업데이트 무신사 크롤링
def ProductsUpdate(Category_list, brand_list):
    for cate in Category_list[0:48]:
        urls = cate['category_link']
        category_id = Category.objects.filter(id=cate['id']) 
        sub_category_name = cate['sub_category_name']
        print(sub_category_name)
        
        # 카테고리 페이지_페이지네이션 최대 페이지 확인
        page_res = requests.get(urls, headers)
        page_res.raise_for_status()
        page_soup = BeautifulSoup(page_res.text, 'lxml')
        page_result = page_soup.find("span", attrs={"class":"totalPagingNum"}).get_text() # 최대 페이지
        # print(page_result)

        category_number = urls[len(urls)-6:]      # 카테고리 번호
        page_number = 3                           # 페이지 수 선택
        if int(page_result) < int(page_number):
            page_number = page_result
        for page in range(1, page_number):        # 1 ~ page_number or 최대 페이지까지 상품 정보 가져오기
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
                    product_double_check = Product.objects.get(product_number=item_number)
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
                        print(f"{brand_name} 정보가 없습니다.")
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
                            
                            try:    
                                # 브랜드 정보
                                brand_id = Brand.objects.get(id=br['id']) 
                                # print(f"{brand_id} / {product_name} / {discount_rate} / {category_id} / {original_price} / {review_count}")
                                
                                instance = Product.objects.create(
                                    brand = brand_id,
                                    product_number = product_number,
                                    product_name = product_name,
                                    product_image = f"https:{product_image}",
                                    original_price = int(original_price),
                                    discount_price = int(discount_price),
                                    review_count = int(review_count)
                                )
                                instance.category.set(category_id)
                            except:
                                print(f"{brand_name} 정보가 없습니다.")
                        else:
                            pass


# 무신사 상품 번호로 상품 등록
def MusinsaNumberProductsCreate(request):

    product_number = request['product_number'] # 등록할 상품 번호

    try: # 중복 체크
        product_double_check = Product.objects.get(product_number=product_number)
        result = "ERROR_01"
        return result
    except: # 신규 상품
        product_double_check = None
        print(f"{product_number} = 신규 상품")
        
    if product_double_check == None: # 신규 상품 처리
    
        product_url = f"https://www.musinsa.com/app/goods/{product_number}"

        res = requests.get(product_url, headers=headers)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'lxml')
        product_info = soup.find('div', attrs={'class':'right_contents'})

        # 상품 카테고리
        categories = product_info.find('p', attrs={'class':'item_categories'})
        a_tag = categories.find_all('a')
        sub = a_tag[1]['href']
        
        # 브랜드명
        brand = a_tag[2].get_text().replace('(', '').replace(')', '').strip()
        
        # 상품 이미지
        product_image = product_info.find('div', attrs={'class':'product-img'}).img['src']
        
        # 상품명
        product_name = product_info.find('span', attrs={'class':'product_title'}).em.get_text()
        
        # 상품 가격
        original_price = product_info.find('li', attrs={'id':'normal_price'}).get_text() # 정상가
        discount_price = product_info.find('span', attrs={'class':'txt_price_member'}).get_text().replace('원', '').replace(',', '') # 할인가
        
        # 상품 리뷰
        review_count = product_info.find('span', attrs={'class':'prd-score__review-count'}).get_text().replace('후기 ', '').replace('개 보기', '')
        try:
            brand_id = Brand.objects.get(brand_name_kr=brand) # 브랜드 DB 연결 준비
            category_id = Category.objects.filter(category_link=sub) # 카테고리 DB 연결 준비
            
            # 상품 등록
            instance = Product.objects.create(
                brand = brand_id,
                product_number = product_number,
                product_name = product_name,
                product_image = f"https:{product_image}",
                original_price = int(original_price),
                discount_price = int(discount_price),
                review_count = int(review_count)
            )
            # 카테고리 DB 연결
            instance.category.set(category_id)
        except:
            print(f"{brand} 정보가 없습니다.")
    else:
        result = "ERROR_02"
        return result

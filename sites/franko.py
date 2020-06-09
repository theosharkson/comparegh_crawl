
def crawl_franko(sc_items,process, fuzz):
	try:
	    element = WebDriverWait(browser, 50,5).until(
	        EC.presence_of_element_located((By.CSS_SELECTOR , 'div[id="js-product-list"]'))
	    )
	except TimeoutException:
		print('Timeout, Wait element not found')
	finally:
		
		try:
			SCROLL_PAUSE_TIME = 2

			# Get scroll height
			last_height = browser.execute_script("return document.body.scrollHeight")

			while True:
			    # Scroll down to bottom
			    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			    time.sleep(1)
			    browser.execute_script("window.scrollTo(0,0);")
			    time.sleep(1)
			    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

			    # Wait to load page
			    time.sleep(SCROLL_PAUSE_TIME)

			    # Calculate new scroll height and compare with last scroll height
			    new_height = browser.execute_script("return document.body.scrollHeight")
			    if new_height == last_height:
			        break
			    last_height = new_height
			
			# time.sleep(sleep_seconds)
			#FIND THE ELEMENTS ON THE PAGE
			products = browser.find_element_by_id('js-product-list').find_elements_by_class_name('item')
			print(len(products))
			for product in products:
				# print(product.get_attribute('innerHTML'))
				name = product.find_element_by_class_name('productName').get_attribute('innerText').strip()
				url = product.find_element_by_class_name('productName').find_element_by_tag_name('a').get_attribute('href')
				price = re.sub('[^0-9.]','',product.find_element_by_css_selector('span[class="price"]').get_attribute('innerText').strip())
				image_url = product.find_element_by_class_name('cover_image').find_element_by_tag_name('img').get_attribute('src').strip()
				
				match = process.extractOne(name, sc_items, scorer=fuzz.token_set_ratio)

				if match[1] > 99:

					print(match)

					pload = {'name': match[0]}
					response = requests.post('http://pricecompare.test/api/sc-item-id-by-name',data = pload)
					print(response.text)
					sc_item_id  = response.text


					print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
					# match = find_match(name,category_id)
					print(url)
					print(name)
					print(price)
					print(image_url)

					print("SC-ITEM-ID : "+sc_item_id)

					# Save Data to DB
					pload = {	
								'merchantid': 3,
								'parent': sc_item_id,
								'name': name,
								'image': image_url,
								'url': url,
								'price': price
							}
					response = requests.post('http://pricecompare.test/products',data = pload)
					print(response.json());

					print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")

				#PROCESS THE DATA COLLECTED INTO THE DATABASE -> the content of process_to_db.py does all the db process
				#NB it should not be moved a step forward or backwards els it would not work
				# exec(compile(source=open('selectors/db/process_to_db.py').read(), filename='process_to_db.py', mode='exec')) 

		except NoSuchElementException:
			print('Timeout, Container not found')
	# print(matched)
	# print(not_matched)


	# Get the next page if any
	try:
		

		next_url_page = browser.find_element_by_css_selector('a[class="next js-search-link"]').get_attribute('href').strip()
		browser.get(next_url_page)
		print("||||||||||||||||||||||||||||||||||||||||||||||||||")
		print("||||||||||||||||||||||||||||||||||||||||||||||||||")
		print("||||||||||||||||||||||||||||||||||||||||||||||||||")

		print(sleep_seconds)
		time.sleep(sleep_seconds)
		

		crawl_franko(sc_items,process, fuzz)
	except NoSuchElementException:
			print('Next Page Button Not Found')



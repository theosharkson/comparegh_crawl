
def crawl_gsmarena():
	try:
	    element = WebDriverWait(browser, 50,5).until(
	        EC.presence_of_element_located((By.CSS_SELECTOR , 'div[class="st-text"]'))
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
			link_tds = browser.find_element_by_class_name('st-text').find_elements_by_tag_name('td')
			print(len(link_tds))
			for td in link_tds:
				
				link = td.find_element_by_tag_name('a').get_attribute('href')
				brand = td.find_element_by_tag_name('a').get_attribute('innerHTML').split("<br>")[0]
				print("====== PAGE ======\n")
				print(link)
				print(brand)
				print("==================\n")
				
				products_browser = webdriver.Firefox()
				getPageProducts(link,products_browser,brand)

		except NoSuchElementException:
			print('Timeout, Container not found')



def getPageProducts(url,products_browser,brand):
	products_browser.get(url)
	try:
	    element = WebDriverWait(products_browser, 50,5).until(
	        EC.presence_of_element_located((By.CSS_SELECTOR , 'div[class="makers"]'))
	    )
	except TimeoutException:
		print('Timeout, Wait element not found')
	finally:
		
		try:
			SCROLL_PAUSE_TIME = 2

			# Get scroll height
			last_height = products_browser.execute_script("return document.body.scrollHeight")

			while True:
			    # Scroll down to bottom
			    products_browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			    time.sleep(1)
			    products_browser.execute_script("window.scrollTo(0,0);")
			    time.sleep(1)
			    products_browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

			    # Wait to load page
			    time.sleep(SCROLL_PAUSE_TIME)

			    # Calculate new scroll height and compare with last scroll height
			    new_height = products_browser.execute_script("return document.body.scrollHeight")
			    if new_height == last_height:
			        break
			    last_height = new_height
			
			# time.sleep(sleep_seconds)
			#FIND THE ELEMENTS ON THE PAGE

			products = products_browser.find_element_by_class_name('makers').find_elements_by_tag_name('li')
			print(len(products))
			for product in products:
				# print(product.get_attribute('innerHTML'))
				name = brand+" "+product.find_element_by_tag_name('a').get_attribute('innerText').strip()
				url = product.find_element_by_tag_name('a').get_attribute('href')
				image_url = product.find_element_by_tag_name('img').get_attribute('src').strip()
				
				print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
				# match = find_match(name,category_id)
				print(name)
				print(url)
				print(image_url)
				print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")

				# Save Data to DB
				pload = {	
							'name': name,
							'image': image_url,
							'category': 1
						}
				response = requests.post('http://pricecompare.test/sc',data = pload)
				print(response.json());

		except NoSuchElementException:
			products_browser.quit()
			print('Timeout, Container not found')
	# print(matched)
	# print(not_matched)


	# Get the next page if any
	try:
		
		next_url_page = products_browser.find_element_by_css_selector('a[class="pages-next"]').get_attribute('href').strip()
		if next_url_page.endswith(".php"):
			# products_browser.get(next_url_page)

			print("||||||||||||||||||||||||||||||||||||||||||||||||||")	
			print(next_url_page)
			print("||||||||||||||||||||||||||||||||||||||||||||||||||")

			# products_browser.quit()
			getPageProducts(next_url_page,products_browser,brand)

			# print(sleep_seconds)
			# time.sleep(sleep_seconds)
			

			
	except NoSuchElementException:
			products_browser.quit()
			print('Next Page Button Not Found')

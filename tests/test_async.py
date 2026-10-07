#work :-->
#navigate to the facebook.com need to validate the (title of the page)
#navigate CMD :-->
#.env requirements file


# from playwright.sync_api import sync_playwright, expect
# #from playwright.async_api import async_playwright, expect
# import asyncio
#sync :-->
#def test_async_sync_exp1():
 # with sync_playwright() as p:
      #chrome browser
       #browser = p.chromium.launch(headless=True)
       #user_context = browser.new_context()
      #page = user_context.new_page()
      #page.goto("https://www.facebook.com/")
      #print(page.title())
      #expect(page).to_have_title("Facebook")


#async def test_async_sync_exp2():
#   async with async_playwright() as p:
#       browser = await p.chromium.launch(headless=True)
#       user_context = await browser.new_context()
#       page = await user_context.new_page()
#       await page.goto("https://www.facebook.com/")
#       print(page.title())
#       await expect(page).to_have_title("Facebook")
#asyncio.run(test_async_sync_exp2())

       #anyio py -m pip install anyio
       #pytest-m pip install pytest-asyncio
       #py -m pip install pytest-asyncio
       
       
      
    
      

 #test :-->banking
 # login as user 
 # login as manager
 #    





# def test_async_sync_exp3(page):
#     page.goto("https://www.google.com/")
#     print(page.title())
#     expect(page).to_have_title("Google")
#     page.goto("https://www.google.com/")
#     expect(page).to_have_url("https://www.google.com/")
#     page.go_back()
#     page.go_forward()
#     page.reload()


    # @pytest.mark.asyncio

    # async def test_async_sync_exp4(page : {goto ,title}):
    #     page = await goto("https://www.facebook.com/")
    #     print(page.title())
    #     await expect(page).to_have_title("Facebook")
    


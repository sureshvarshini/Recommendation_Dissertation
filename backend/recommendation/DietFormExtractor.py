# from bs4 import BeautifulSoup
# from requests_html import HTMLSession
# from pprint import pprint
# import requests
# import urllib
# from urllib.request import urlopen
# from urllib.parse import urlencode
# import webbrowser

# # Start HTTP session
# session = HTMLSession()
# # url = 'https://www.nal.usda.gov/human-nutrition-and-food-safety/dri-calculator'
# url = 'https://wikipedia.org'

# def get_dri_form():

#     res = session.get(url)
#     # res.html.render()
#     soup = BeautifulSoup(res.html.html, "html.parser")
#     return soup.find_all("form")


# def get_dri_form_details(form):
#     print(form)
#     details = {}
#     action = form
#     print("----------> ACTION")
#     print(action)

#     if action:
#         action = action.lower()

#     method = form.attrs.get("method", "get").lower()

#     inputs = []
#     for input_tag in form.find_all("input"):
#         # get type of input form control
#         input_type = input_tag.attrs.get("type", "text")
#         # get name attribute
#         input_name = input_tag.attrs.get("name")
#         # get the default value of that input tag
#         input_value =input_tag.attrs.get("value", "")
#         # add everything to that list
#         inputs.append({"type": input_type, "name": input_name, "value": input_value})
#     for select in form.find_all("select"):
#         # get the name attribute
#         select_name = select.attrs.get("name")
#         # set the type as select
#         select_type = "select"
#         select_options = []
#         # the default select value
#         select_default_value = ""
#         # iterate over options and get the value of each
#         for select_option in select.find_all("option"):
#             # get the option value used to submit the form
#             option_value = select_option.attrs.get("value")
#             if option_value:
#                 select_options.append(option_value)
#                 if select_option.attrs.get("selected"):
#                     # if 'selected' attribute is set, set this option as default    
#                     select_default_value = option_value
#         if not select_default_value and select_options:
#             # if the default is not set, and there are options, take the first option as default
#             select_default_value = select_options[0]
#         # add the select to the inputs list
#         inputs.append({"type": select_type, "name": select_name, "values": select_options, "value": select_default_value})
#     for textarea in form.find_all("textarea"):
#         # get the name attribute
#         textarea_name = textarea.attrs.get("name")
#         # set the type as textarea
#         textarea_type = "textarea"
#         # get the textarea value
#         textarea_value = textarea.attrs.get("value", "")
#         # add the textarea to the inputs list
#         inputs.append({"type": textarea_type, "name": textarea_name, "value": textarea_value})
        
#     # put everything to the resulting dictionary
#     details["action"] = action
#     details["method"] = method
#     details["inputs"] = inputs
#     return details


# def submit_form(user): - not working

#     payload = urlencode({
#         'Measurement Unit': 'Metric',
#         'Sex': 'Female',
#         'Age': 89,
#         'Height': 180,
#         'Weight': 70,
#         'Activity level': 'Sedentary',
#         'Pregnancy/Lactation status': 'Not Pregnant or Lactating'
#     })

#     url = 'https://www.nal.usda.gov/human-nutrition-and-food-safety/dri-calculator' + '?' + payload

#     web_response = urlopen(url)

#     print("----> WEB RESPONSE")
#     print(str(web_response.getcode()))
#     with open("results.html", "wb") as f:
#         f.write(web_response.read())
#     webbrowser.open("results.html")


# if __name__ == "__main__":
#     dri_form = get_dri_form()
#     get_dri_form_details(dri_form)

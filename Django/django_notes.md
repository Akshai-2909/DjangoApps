**What is manage.py?**

**path function**: 

- Having Four arguments: 
		* Must : route and view
		* Optional : kwargs and name
			1.**Route**:
				- String contains URL pattern, Django goes from top to down pattern in the urlpatterns comparing the requested with the url that presents in the list.
				- patterns don't search for the GET, POST parameters
			2. **View**:
				If(matchedPatterns):
					Django calls view function with an httpsrequeset object.


** What is migrate?**
migrate = this command looks at  the installed apps in settinhs and create a necessary database tables according to the database settings in setting.py
# Adidas-Account-Generator
Adidas account generator with 2captcha support by [@Acez428](https://twitter.com/Acez428)

# Modified version of https://github.com/bopped/Adidas-Account-Creator by @bopped
* View the readme there for instructions 

# Once you've read the above readme here's what you can do: 


config.json example
``` 
{
    "INFO":{
        "First_Name":"Micah",
        "Last_Name":"Jones",
        "Month":"3",
        "Day":"4",
        "Year":"1994",
        "Email":"mygmailaccount@gmail.com", //gmail account for dot generation
        "Password":"password"
    },
	"createMode" : "catchall", // Valid options are: catchall or gmail
	"base_email" : "beta", // Base for catchall email
	"domain" : "@mycatchall.com", // Domain for catchall email
	"sitekey" : "6LdyFRkUAAAAAF2YmQ9baZ6ytpVnbVSAymVpTXKi", // Sitekey for registration page
	"APIKEY_2CAP" : "YOUR_2CAPTCHA_API_KEY", // Your API key
	"pageurl" : "https://cp.adidas.com/" // Registration endpoint
}

``` 

config.json explaination 
* createMode 
    * `catchall` or `gmail` 
* base_email 
    * If using catchall, this will be the prefix for any generated accounts 
    * The generated account will have the format: `base_email` + `random digits` @ `domain`
* domain 
    * The domain of your catchall 
* sitekey 
    * The sitekey for the registration form 
* APIKEY_2CAP 
    * Your 2captcha api key 

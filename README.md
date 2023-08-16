# Finch Collector Lab Parts 1 - 5
### Django Framework & Python
---
```
**Instructions:**
1. Lab Part 1: https://git.generalassemb.ly/SEI-CC/SEI-6-5/blob/main/Unit_4/3-django/3.2.1-finch-collector-lab-part-1.md
2. Lab Part 2: https://git.generalassemb.ly/SEI-CC/SEI-6-5/blob/main/Unit_4/3-django/3.3.1-finch-collector-lab-part-2.md
3. Lab Part 3: https://git.generalassemb.ly/SEI-CC/SEI-6-5/blob/main/Unit_4/3-django/3.4.1-finch-collector-lab-part-3.md
4. Lab Part 4: https://git.generalassemb.ly/SEI-CC/SEI-6-5/blob/main/Unit_4/3-django/3.5.1-finch-collector-lab-part-4.md
5. Lab Part 5: https://git.generalassemb.ly/SEI-CC/SEI-6-5/blob/main/Unit_4/3-django/3.6.1-finch-collector-lab-part-5.md
```

```
**Django 101:**
- Django follows MVT (model, view, template) pattern, similar to MVC (model, view, controller) in Express.js. Django is also strongly opinionated compared to Express.js, which leaves the implementation of the MVC up to the developer. 
    - Model (M): Django models define structure of database tables, relationships between them, and the methods to interact with the data. Models translate to database schemas and handle the data logic. Usually, if you can fit functionality in the model, you should as you want to adhere to the 'fat models, skinny views' philosophy

    - View (V): Django views are more like controllers in the classic MVC framework. Views in Django handle business logic, receive HTTP requests, interact with models, and return HTTP responses. They are the entry point for any functionality in the application.

    - Template (T): Django templates are similar to views in MVC, but utilizes Django Template Language (DTL) to allow for dyanamic rendering of content on the front-end.
- Django is written in Python, but DTL is **not** embedded Python like JSX is embedded JavaScript. 
- URL routing is defined in their respective urls.py files, where we map URLs to specific view functions and assign a name. urls.py file in the root level (ex. finchcollector/) store program wide routes like /admin. While the same file in the application level folder (ex. main_app/) stores application wide routes like 'app/create/', or '/app/'.
```

```
**Models in Django**
```
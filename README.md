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


### Django 101:
- Django follows MVT (model, view, template) pattern, similar to MVC (model, view, controller) in Express.js. Django is also strongly opinionated compared to Express.js, which leaves the implementation of the MVC up to the developer. 
    - Model (M): Django models define structure of database tables, relationships between them, and the methods to interact with the data. Models translate to database schemas and handle the data logic. Usually, if you can fit functionality in the model, you should as you want to adhere to the 'fat models, skinny views' philosophy

    - View (V): Django views are more like controllers in the classic MVC framework. Views in Django handle business logic, receive HTTP requests, interact with models, and return HTTP responses. They are the entry point for any functionality in the application.

    - Template (T): Django templates are similar to views in MVC, but utilizes Django Template Language (DTL) to allow for dyanamic rendering of content on the front-end.
- Django is written in Python, but DTL is *not* embedded Python like JSX is embedded JavaScript. 
- URL routing is defined in their respective urls.py files, where we map URLs to specific view functions and assign a name. urls.py file in the root level (ex. finchcollector/) store program wide routes like /admin. While the same file in the application level folder (ex. main_app/) stores application wide routes like 'app/create/', or '/app/'.

---

**Models in Django**
- Django models use Python class and inherits from: 'django.db.models.Model' where each attribute of the class is a field in the database table and the type of that field is the value assigned to the key.
    ```
    from django.db import models

    class Book(models.Model):
        title = models.CharField(max_length=200)
        author = models.ForeignKey('Author', on_delete=models.CASCADE)
        published_date = models.DateField()
        is_published = models.BooleanField(default=False)

    ```
- DataTypes for the fields are as follows:
    ```
        - CharField: A string field, for short- to medium-length strings.
        - IntegerField: An integer field.
        - DateTimeField: A date and time field.
        - ForeignKey: For creating one-to-many relationships.
        - ManyToManyField: For creating many-to-many relationships.
        - ImageField, FileField: For handling files and images.
    ```
- These relationships can be defined between tables:
    - One-to-Many: 
        > Use ForeignKey to create a one-to-many relationship between two models.
        ```
        class Feeding(models.Model):
            date = models.DateField()
            # this will create a select menu on the form
            # where the choices are the elements of the MEALS
            # tuple, & default value is 'B','Breakfast'
            meal = models.CharField(max_length=1, 
                                    choices = MEALS, 
                                    default = MEALS[0][0])
            # create a cat_id FK; it will automatically add _id to key name
            # on_delete = models.CASCADE is required 
            # in a one:many relationship bc it ensures that 
            # children are also removed when a parent (cat) record is deleted
            finch = models.ForeignKey(Finch, on_delete=models.CASCADE)
        ```

    - Many-to-Many: 
        > Use ManyToManyField to create a many-to-many relationship between models.
        ```
        class Finch(models.Model):
            # name of Finch can be nullable
            name = models.CharField(max_length=100, null=True)
            breed = models.CharField(max_length=100)
            description = models.TextField(max_length=250)
            age = models.IntegerField()
            toys = models.ManyToManyField(Toy)
        ```
    - One-to-One: 
        > Use OneToOneField to create a one-to-one relationship between models.
        ```
        class Finch(models.Model):
            name = models.CharField(max_length=50)
            color = models.CharField(max_length=30)
            nest = models.OneToOneField(Nest, on_delete=models.CASCADE, related_name='finch')

            def __str__(self):
                return self.name
        ```
- You can define a **Meta** class inside a Django model to define various metadata and behavioral aspects:
    - 'ordering':
        > defines the default ordering for queries; similar to .sort()
        ```
        class Finch(models.Model):
        name = models.CharField(max_length=50)
        age = models.IntegerField()

        class Meta:
            ordering = ['name']  # Orders by name alphabetically
        ```
    - 'verbose_name' or 'verbose_name_plural': 
        > custom names for the model in the admin interface
        ```  
        class Meta:
            verbose_name = 'Finch Bird'
            verbose_name_plural = 'Finch Birds' 
        ```
    - 'indexes': 
        > custom database index
        ```
        class Finch(models.Model):
            species = models.CharField(max_length=50)

        class Meta:
            indexes = [
                models.Index(fields=['species']),
        ]
        ```
    - 'unique_together':
        > constraints for unique combinations of fields
        ```
        class Finch(models.Model):
            name = models.CharField(max_length=50)
            ring_number = models.CharField(max_length=10)

        class Meta:
            unique_together = ('name', 'ring_number',)
        ```
    - 'permissions':
        > define custom permissions for the model, used in conjunction with Django's auth system
        ```
        class Meta:
            permissions = [
                ("view_finch", "Can view finch"),
            ]

        ```
    - 'db_table':
        > define a custom db table name for the model
        ```        
        class Meta:
            db_table = 'custom_finch_table'
        ```

**Migrations**
- Changes or updates to models require the following commands to be run:
    1. >python3 manage.py makemigrations
    2. >python3 manage.py migrate
- To see all migrations:
    - >python3 manage.py showmigrations

**Querying**
- Django models can be queried. Here are some examples:
- Get All
    > all_var = Model.objects.all()
- Find by PK
    > var = Model.objects.get(pk=*n*)
- Filtering
    > var = Model.objects.filter(<field1>=<condition1>)
    > var_excludes = Model.objects.exclude(<field1>=<condition1>)
- Chaining:
    > var_name = Model.objects.filter(<field1>:<condition1>, <field2>:<condition2>).order_by('-<field>)
- Aggregating:
    ```
    from django.db.models import Avg

    avg_var = Model.objects.all().aggregate(Avg(<field1>))
    ```
- Conditional Lookups:
    ```
    from django.db.models import Q

    # get objects that satify condition 1 OR condition 2
    var = Model.objects.filter(Q(<field1>=<condition1> | Q(<field2__gt>=<n>)))
    ```
- Pagination:
    ```
    from django.core.paginator import Paginator
    # limit to 5 objects per page
    paginator = Paginator(Model.objects.all(),5)
    page = paginator.get_page(1) # get first page
    ```
- Annotations:
    ```
    from django.db.models import Count

    var = Model.objects.annotate(num_var=Count(<field1>))
    ```
- Raw SQL:
    ```
    from django.db import connection

    # '%s' passes variables from outside the SQL statement
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM db_table WHERE <field1> > %s', [5])
        results = cursor.fetchall()
    ```
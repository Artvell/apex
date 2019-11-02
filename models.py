# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class RolesCategories(models.Model):
    category = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'roles_categories'


class RolesCodes(models.Model):
    shtrih = models.CharField(max_length=50)
    kolvo = models.FloatField()
    name = models.ForeignKey('RolesProducts', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles_codes'


class RolesConsuption(models.Model):

    class Meta:
        managed = False
        db_table = 'roles_consuption'


class RolesDopMoney(models.Model):
    money = models.IntegerField()
    dop_type = models.ForeignKey('RolesDopTypes', models.DO_NOTHING)
    nak_id = models.ForeignKey('RolesPurchase', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'roles_dop_money'


class RolesDopTypes(models.Model):
    name = models.CharField(max_length=50)
    min_summ = models.IntegerField()
    max_summ = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'roles_dop_types'


class RolesIngredients(models.Model):
    kolvo = models.FloatField()
    ingr = models.ForeignKey('RolesProducts', models.DO_NOTHING)
    product = models.ForeignKey('RolesProducts', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'roles_ingredients'


class RolesIngredientsDopInfo(models.Model):
    srok = models.FloatField()
    procent = models.FloatField()
    product = models.ForeignKey('RolesProducts', models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'roles_ingredients_dop_info'


class RolesLastcost(models.Model):
    cost = models.FloatField()
    product = models.ForeignKey('RolesProducts', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'roles_lastcost'


class RolesMoney(models.Model):
    dat = models.DateField()
    dsumma = models.IntegerField()
    is_calculated = models.IntegerField()
    isumma = models.IntegerField()
    nak_id = models.CharField(max_length=37)
    nsumma = models.IntegerField()
    psumma = models.IntegerField()
    rsumma = models.IntegerField()
    vsumma = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'roles_money'


class RolesMoneyReceivers(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'roles_money_receivers'


class RolesMoneys(models.Model):
    kolvo = models.FloatField()
    types = models.ForeignKey('RolesTypesOfMoney', models.DO_NOTHING, unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles_moneys'


class RolesNaklForZagot(models.Model):
    tkolvo = models.FloatField()
    is_accepted = models.IntegerField()
    pkolvo = models.FloatField()
    price = models.FloatField()
    summ = models.FloatField()
    is_maked = models.IntegerField()
    ac_kolvo = models.FloatField()
    srok = models.DateTimeField(blank=True, null=True)
    in_stock = models.IntegerField()
    name = models.ForeignKey('RolesProducts', models.DO_NOTHING)
    nak_id = models.IntegerField()
    shtrih = models.CharField(max_length=20)
    user = models.ForeignKey('RolesZagotTypes', models.DO_NOTHING)
    is_returned = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'roles_nakl_for_zagot'


class RolesNaklMoneyOther(models.Model):
    name = models.CharField(max_length=20)
    for_why = models.TextField()
    kolvo = models.FloatField()
    types = models.ForeignKey('RolesTypesOfMoney', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles_nakl_money_other'


class RolesNaklMoneyZakup(models.Model):
    kolvo = models.FloatField()
    name = models.ForeignKey(AuthUser, models.DO_NOTHING)
    types = models.ForeignKey('RolesTypesOfMoney', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles_nakl_money_zakup'


class RolesPizzerias(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'roles_pizzerias'


class RolesPostavsh(models.Model):
    firm_name = models.CharField(max_length=50)
    name = models.CharField(unique=True, max_length=20)
    contact = models.CharField(max_length=50)
    place = models.TextField()

    class Meta:
        managed = False
        db_table = 'roles_postavsh'


class RolesProducts(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    prigot = models.IntegerField()
    edizm = models.ForeignKey('RolesUnits', models.DO_NOTHING, blank=True, null=True)
    maks_zakup = models.IntegerField()
    min_zakup = models.IntegerField()
    rashod = models.FloatField()
    artikul = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'roles_products'


class RolesPurchase(models.Model):
    nak_id = models.CharField(max_length=50)
    last_cost = models.FloatField()
    kolvo = models.FloatField()
    is_accepted = models.IntegerField()
    purchased_kol = models.FloatField()
    new_cost = models.FloatField()
    summ = models.FloatField()
    fact_kol = models.FloatField()
    srok = models.DateField(blank=True, null=True)
    is_delivered = models.IntegerField()
    name = models.ForeignKey(RolesProducts, models.DO_NOTHING)
    min_srok = models.DateField(blank=True, null=True)
    is_accepted_zakup = models.IntegerField()
    purchase = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    is_returned = models.IntegerField()
    date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles_purchase'


class RolesRashodZagot(models.Model):
    kol = models.IntegerField()
    nak_id = models.ForeignKey(RolesNaklForZagot, models.DO_NOTHING)
    name = models.ForeignKey(RolesProducts, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'roles_rashod_zagot'


class RolesReceivers(models.Model):
    receiver = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'roles_receivers'


class RolesRoles(models.Model):
    role = models.IntegerField(blank=True, null=True)
    place = models.ForeignKey(RolesPizzerias, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'roles_roles'


class RolesSalers(models.Model):
    last_cost = models.FloatField()
    product = models.ForeignKey(RolesProducts, models.DO_NOTHING)
    saler = models.ForeignKey(RolesPostavsh, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'roles_salers'


class RolesSpis(models.Model):
    i = models.AutoField(primary_key=True)
    nak_id = models.IntegerField()
    user = models.CharField(max_length=20)
    product = models.CharField(max_length=100)
    kol = models.FloatField()
    date = models.DateField(blank=True, null=True)
    receiver = models.ForeignKey(RolesReceivers, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'roles_spis'


class RolesStock(models.Model):
    ostat = models.FloatField()
    name = models.ForeignKey(RolesProducts, models.DO_NOTHING, unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles_stock'


class RolesTypesOfMoney(models.Model):
    types = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'roles_types_of_money'


class RolesUnits(models.Model):
    edizm = models.CharField(max_length=20)
    opis = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'roles_units'


class RolesZagotTypes(models.Model):
    product = models.ForeignKey(RolesProducts, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'roles_zagot_types'


class RolesZakupshiki(models.Model):
    name = models.ForeignKey(RolesProducts, models.DO_NOTHING, unique=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'roles_zakupshiki'

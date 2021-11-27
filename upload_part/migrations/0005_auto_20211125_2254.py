# Generated by Django 3.2.8 on 2021-11-25 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload_part', '0004_auto_20211125_2226'),
    ]

    operations = [
        migrations.RenameField(
            model_name='advertisingcosts',
            old_name='retty',
            new_name='ad11',
        ),
        migrations.RenameField(
            model_name='advertisingcosts',
            old_name='maipure',
            new_name='ad13',
        ),
        migrations.RenameField(
            model_name='advertisingcosts',
            old_name='externalSalesCost',
            new_name='ad14',
        ),
        migrations.RenameField(
            model_name='advertisingcosts',
            old_name='googleAds',
            new_name='ad16',
        ),
        migrations.RenameField(
            model_name='advertisingcosts',
            old_name='jobAds',
            new_name='ad17',
        ),
        migrations.RenameField(
            model_name='advertisingcosts',
            old_name='advertisingGurunabi',
            new_name='ad2',
        ),
        migrations.RenameField(
            model_name='advertisingcosts',
            old_name='Gurunabi',
            new_name='ad3',
        ),
        migrations.RenameField(
            model_name='advertisingcosts',
            old_name='advertisingHotpepper',
            new_name='ad4',
        ),
        migrations.RenameField(
            model_name='advertisingcosts',
            old_name='Hotpepper',
            new_name='ad5',
        ),
        migrations.RenameField(
            model_name='advertisingcosts',
            old_name='advertisingTabelog',
            new_name='ad6',
        ),
        migrations.RenameField(
            model_name='advertisingcosts',
            old_name='Tabelog',
            new_name='ad7',
        ),
        migrations.RenameField(
            model_name='drinkcosts',
            old_name='drinkOther',
            new_name='drink11',
        ),
        migrations.RenameField(
            model_name='laborcosts',
            old_name='labor_costs',
            new_name='labor2',
        ),
        migrations.RenameField(
            model_name='laborcosts',
            old_name='employee_costs',
            new_name='labor3',
        ),
        migrations.RenameField(
            model_name='laborcosts',
            old_name='partTimeWorker_costs',
            new_name='labor4',
        ),
        migrations.RenameField(
            model_name='laborcosts',
            old_name='company_insurance_total',
            new_name='labor5',
        ),
        migrations.RenameField(
            model_name='laborcosts',
            old_name='other_ex_dailyPayment',
            new_name='labor6',
        ),
        migrations.RenameField(
            model_name='laborcosts',
            old_name='other_ex_dailyPayment2',
            new_name='labor7',
        ),
        migrations.RenameField(
            model_name='laborcosts',
            old_name='bonus',
            new_name='labor8',
        ),
        migrations.RenameField(
            model_name='laborcosts',
            old_name='transportationExpenses',
            new_name='labor9',
        ),
        migrations.RenameField(
            model_name='othercosts',
            old_name='pestControl',
            new_name='other11',
        ),
        migrations.RenameField(
            model_name='othercosts',
            old_name='meetingCost',
            new_name='other16',
        ),
        migrations.RenameField(
            model_name='othercosts',
            old_name='inspectionCost',
            new_name='other17',
        ),
        migrations.RenameField(
            model_name='othercosts',
            old_name='entertainmentFee',
            new_name='other18',
        ),
        migrations.RenameField(
            model_name='othercosts',
            old_name='welfare',
            new_name='other19',
        ),
        migrations.RenameField(
            model_name='othercosts',
            old_name='askul',
            new_name='other2',
        ),
        migrations.RenameField(
            model_name='othercosts',
            old_name='capitalInvestment',
            new_name='other20',
        ),
        migrations.RenameField(
            model_name='othercosts',
            old_name='housingAllowance',
            new_name='other21',
        ),
        migrations.RenameField(
            model_name='othercosts',
            old_name='companyHousingAllowance',
            new_name='other22',
        ),
        migrations.RenameField(
            model_name='othercosts',
            old_name='parkingLot',
            new_name='other23',
        ),
        migrations.RenameField(
            model_name='othercosts',
            old_name='vehicleCost',
            new_name='other24',
        ),
        migrations.RenameField(
            model_name='othercosts',
            old_name='labor_and_social_security_attorney',
            new_name='other25',
        ),
        migrations.RenameField(
            model_name='othercosts',
            old_name='tax_accountant',
            new_name='other26',
        ),
        migrations.RenameField(
            model_name='othercosts',
            old_name='update2',
            new_name='other27',
        ),
        migrations.RenameField(
            model_name='othercosts',
            old_name='update',
            new_name='other28',
        ),
        migrations.RenameField(
            model_name='othercosts',
            old_name='subsidy',
            new_name='other29',
        ),
        migrations.RenameField(
            model_name='othercosts',
            old_name='expendables2',
            new_name='other4',
        ),
        migrations.RenameField(
            model_name='othercosts',
            old_name='regiLease',
            new_name='other5',
        ),
        migrations.RenameField(
            model_name='othercosts',
            old_name='other',
            new_name='other7',
        ),
        migrations.RenameField(
            model_name='othercosts',
            old_name='expendables3',
            new_name='other8',
        ),
        migrations.RenameField(
            model_name='othercosts',
            old_name='garbageDisposal',
            new_name='other9',
        ),
        migrations.RenameField(
            model_name='taxexemptexpenses',
            old_name='insuranceFee',
            new_name='tax1',
        ),
        migrations.RenameField(
            model_name='taxexemptexpenses',
            old_name='taxEffect',
            new_name='tax13',
        ),
        migrations.RenameField(
            model_name='taxexemptexpenses',
            old_name='insuranceFee_store_industrialAccident',
            new_name='tax14',
        ),
        migrations.RenameField(
            model_name='taxexemptexpenses',
            old_name='insuranceFee_car_inspection',
            new_name='tax15',
        ),
        migrations.RenameField(
            model_name='taxexemptexpenses',
            old_name='bankruptcy_prevention',
            new_name='tax16',
        ),
        migrations.RenameField(
            model_name='taxexemptexpenses',
            old_name='insuranceFee2',
            new_name='tax2',
        ),
        migrations.RenameField(
            model_name='taxexemptexpenses',
            old_name='repayment',
            new_name='tax3',
        ),
        migrations.RenameField(
            model_name='taxexemptexpenses',
            old_name='repayment1',
            new_name='tax5',
        ),
        migrations.RenameField(
            model_name='taxexemptexpenses',
            old_name='repayment2',
            new_name='tax6',
        ),
        migrations.RenameField(
            model_name='taxexemptexpenses',
            old_name='repayment3',
            new_name='tax7',
        ),
        migrations.RenameField(
            model_name='taxexemptexpenses',
            old_name='repayment4',
            new_name='tax8',
        ),
        migrations.RenameField(
            model_name='utilitycosts_comunicationcosts',
            old_name='waterSavingCost',
            new_name='util10',
        ),
        migrations.RenameField(
            model_name='utilitycosts_comunicationcosts',
            old_name='communicationCost',
            new_name='util12',
        ),
        migrations.RenameField(
            model_name='utilitycosts_comunicationcosts',
            old_name='internetFee',
            new_name='util15',
        ),
        migrations.RenameField(
            model_name='utilitycosts_comunicationcosts',
            old_name='willcom',
            new_name='util18',
        ),
        migrations.RenameField(
            model_name='utilitycosts_comunicationcosts',
            old_name='gasFee',
            new_name='util2',
        ),
        migrations.RenameField(
            model_name='utilitycosts_comunicationcosts',
            old_name='electricBill',
            new_name='util3',
        ),
        migrations.RenameField(
            model_name='utilitycosts_comunicationcosts',
            old_name='waterBill',
            new_name='util4',
        ),
        migrations.RenameField(
            model_name='utilitycosts_comunicationcosts',
            old_name='sewerBill',
            new_name='util5',
        ),
        migrations.RenameField(
            model_name='utilitycosts_comunicationcosts',
            old_name='electricSavingCost',
            new_name='util6',
        ),
        migrations.RemoveField(
            model_name='advertisingcosts',
            name='chibadoyukai',
        ),
        migrations.RemoveField(
            model_name='advertisingcosts',
            name='externalSalesCost_googleAds',
        ),
        migrations.RemoveField(
            model_name='advertisingcosts',
            name='fesMaipure_recoru',
        ),
        migrations.RemoveField(
            model_name='advertisingcosts',
            name='hitosara_gururiza',
        ),
        migrations.RemoveField(
            model_name='advertisingcosts',
            name='roi_recoruHeadquarters',
        ),
        migrations.RemoveField(
            model_name='advertisingcosts',
            name='tLab',
        ),
        migrations.RemoveField(
            model_name='drinkcosts',
            name='altcorporationWine',
        ),
        migrations.RemoveField(
            model_name='drinkcosts',
            name='hashimoto',
        ),
        migrations.RemoveField(
            model_name='drinkcosts',
            name='izumiyaDrink',
        ),
        migrations.RemoveField(
            model_name='drinkcosts',
            name='kakuyasuDrink',
        ),
        migrations.RemoveField(
            model_name='drinkcosts',
            name='nestle',
        ),
        migrations.RemoveField(
            model_name='drinkcosts',
            name='pieroth',
        ),
        migrations.RemoveField(
            model_name='drinkcosts',
            name='yatsuya',
        ),
        migrations.RemoveField(
            model_name='drinkcosts',
            name='yatsuya_jenos',
        ),
        migrations.RemoveField(
            model_name='drinkcosts',
            name='yatsuya_jenos2',
        ),
        migrations.RemoveField(
            model_name='othercosts',
            name='altcorporation',
        ),
        migrations.RemoveField(
            model_name='othercosts',
            name='dyfil',
        ),
        migrations.RemoveField(
            model_name='othercosts',
            name='expendables',
        ),
        migrations.RemoveField(
            model_name='othercosts',
            name='prenty',
        ),
        migrations.RemoveField(
            model_name='othercosts',
            name='saniclean_drainagePipe',
        ),
        migrations.RemoveField(
            model_name='othercosts',
            name='toyoEnterprise',
        ),
        migrations.RemoveField(
            model_name='othercosts',
            name='wetTowel_ootaki',
        ),
        migrations.RemoveField(
            model_name='taxexemptexpenses',
            name='creditCard_chibabank2',
        ),
        migrations.RemoveField(
            model_name='taxexemptexpenses',
            name='creditCard_rakuten',
        ),
        migrations.RemoveField(
            model_name='taxexemptexpenses',
            name='creditCard_rakuten2',
        ),
        migrations.RemoveField(
            model_name='taxexemptexpenses',
            name='creditCard_rakutensmp1',
        ),
        migrations.RemoveField(
            model_name='taxexemptexpenses',
            name='creditCard_zentoshin',
        ),
        migrations.RemoveField(
            model_name='taxexemptexpenses',
            name='creditCard_zentoshin2',
        ),
        migrations.RemoveField(
            model_name='taxexemptexpenses',
            name='insuranceFee_fesRepayment',
        ),
        migrations.RemoveField(
            model_name='taxexemptexpenses',
            name='prudential1',
        ),
        migrations.RemoveField(
            model_name='taxexemptexpenses',
            name='prudential2',
        ),
        migrations.RemoveField(
            model_name='utilitycosts_comunicationcosts',
            name='electricSavingCost_lifest',
        ),
        migrations.RemoveField(
            model_name='utilitycosts_comunicationcosts',
            name='electricSavingCost_lifest_arc',
        ),
        migrations.RemoveField(
            model_name='utilitycosts_comunicationcosts',
            name='electricSavingCost_softbank',
        ),
        migrations.RemoveField(
            model_name='utilitycosts_comunicationcosts',
            name='ubiregi',
        ),
        migrations.RemoveField(
            model_name='utilitycosts_comunicationcosts',
            name='ubiregi_nhk',
        ),
        migrations.RemoveField(
            model_name='utilitycosts_comunicationcosts',
            name='usen',
        ),
        migrations.RemoveField(
            model_name='utilitycosts_comunicationcosts',
            name='wanaNakameguroLoan',
        ),
        migrations.RemoveField(
            model_name='utilitycosts_comunicationcosts',
            name='wanaNakameguroLoan_gasFee',
        ),
        migrations.RemoveField(
            model_name='utilitycosts_comunicationcosts',
            name='waterSavingCost_wanaNakameguroLoan',
        ),
        migrations.RemoveField(
            model_name='utilitycosts_comunicationcosts',
            name='willcom_yumeyaLicenseFee',
        ),
        migrations.RemoveField(
            model_name='utilitycosts_comunicationcosts',
            name='yumeyaLicenseFee',
        ),
        migrations.AddField(
            model_name='advertisingcosts',
            name='ad10',
            field=models.IntegerField(blank=True, null=True, verbose_name='本部'),
        ),
        migrations.AddField(
            model_name='advertisingcosts',
            name='ad12',
            field=models.IntegerField(blank=True, null=True, verbose_name='本部'),
        ),
        migrations.AddField(
            model_name='advertisingcosts',
            name='ad15',
            field=models.IntegerField(blank=True, null=True, verbose_name='外販委託料'),
        ),
        migrations.AddField(
            model_name='advertisingcosts',
            name='ad18',
            field=models.IntegerField(blank=True, null=True, verbose_name='会費'),
        ),
        migrations.AddField(
            model_name='advertisingcosts',
            name='ad8',
            field=models.IntegerField(blank=True, null=True, verbose_name='広告費（ぐるなび更新）'),
        ),
        migrations.AddField(
            model_name='advertisingcosts',
            name='ad9',
            field=models.IntegerField(blank=True, null=True, verbose_name='トサラ'),
        ),
        migrations.AddField(
            model_name='drinkcosts',
            name='drink10',
            field=models.IntegerField(blank=True, null=True, verbose_name='酒のさかもと'),
        ),
        migrations.AddField(
            model_name='drinkcosts',
            name='drink2',
            field=models.IntegerField(blank=True, null=True, verbose_name='藤川リカー'),
        ),
        migrations.AddField(
            model_name='drinkcosts',
            name='drink3',
            field=models.IntegerField(blank=True, null=True, verbose_name='山野酒店'),
        ),
        migrations.AddField(
            model_name='drinkcosts',
            name='drink4',
            field=models.IntegerField(blank=True, null=True, verbose_name='ネス'),
        ),
        migrations.AddField(
            model_name='drinkcosts',
            name='drink5',
            field=models.IntegerField(blank=True, null=True, verbose_name='大崎商店'),
        ),
        migrations.AddField(
            model_name='drinkcosts',
            name='drink6',
            field=models.IntegerField(blank=True, null=True, verbose_name='大崎商店'),
        ),
        migrations.AddField(
            model_name='drinkcosts',
            name='drink7',
            field=models.IntegerField(blank=True, null=True, verbose_name='大崎商店'),
        ),
        migrations.AddField(
            model_name='drinkcosts',
            name='drink8',
            field=models.IntegerField(blank=True, null=True, verbose_name='マキコーポレーション'),
        ),
        migrations.AddField(
            model_name='drinkcosts',
            name='drink9',
            field=models.IntegerField(blank=True, null=True, verbose_name='ピージャパン'),
        ),
        migrations.AddField(
            model_name='othercosts',
            name='other10',
            field=models.IntegerField(blank=True, null=True, verbose_name='お絞り代'),
        ),
        migrations.AddField(
            model_name='othercosts',
            name='other12',
            field=models.IntegerField(blank=True, null=True, verbose_name='排水管清掃'),
        ),
        migrations.AddField(
            model_name='othercosts',
            name='other13',
            field=models.IntegerField(blank=True, null=True, verbose_name='ダフィル'),
        ),
        migrations.AddField(
            model_name='othercosts',
            name='other14',
            field=models.IntegerField(blank=True, null=True, verbose_name='アルト'),
        ),
        migrations.AddField(
            model_name='othercosts',
            name='other15',
            field=models.IntegerField(blank=True, null=True, verbose_name='設備リース'),
        ),
        migrations.AddField(
            model_name='othercosts',
            name='other3',
            field=models.IntegerField(blank=True, null=True, verbose_name='プレティ'),
        ),
        migrations.AddField(
            model_name='othercosts',
            name='other6',
            field=models.IntegerField(blank=True, null=True, verbose_name='消耗品'),
        ),
        migrations.AddField(
            model_name='taxexemptexpenses',
            name='tax10',
            field=models.IntegerField(blank=True, null=True, verbose_name='②プデシル'),
        ),
        migrations.AddField(
            model_name='taxexemptexpenses',
            name='tax11',
            field=models.IntegerField(blank=True, null=True, verbose_name='①クレジットカード手数料'),
        ),
        migrations.AddField(
            model_name='taxexemptexpenses',
            name='tax12',
            field=models.IntegerField(blank=True, null=True, verbose_name='②クレジットカード手数料'),
        ),
        migrations.AddField(
            model_name='taxexemptexpenses',
            name='tax17',
            field=models.IntegerField(blank=True, null=True, verbose_name='クレジットカード手数料'),
        ),
        migrations.AddField(
            model_name='taxexemptexpenses',
            name='tax18',
            field=models.IntegerField(blank=True, null=True, verbose_name='クレジットカード手数料'),
        ),
        migrations.AddField(
            model_name='taxexemptexpenses',
            name='tax19',
            field=models.IntegerField(blank=True, null=True, verbose_name='クレジットカード手数料'),
        ),
        migrations.AddField(
            model_name='taxexemptexpenses',
            name='tax20',
            field=models.IntegerField(blank=True, null=True, verbose_name='クレジットカード手数料'),
        ),
        migrations.AddField(
            model_name='taxexemptexpenses',
            name='tax4',
            field=models.IntegerField(blank=True, null=True, verbose_name='保険料/（店舗・自動車・労災）'),
        ),
        migrations.AddField(
            model_name='taxexemptexpenses',
            name='tax9',
            field=models.IntegerField(blank=True, null=True, verbose_name='①プデシル'),
        ),
        migrations.AddField(
            model_name='utilitycosts_comunicationcosts',
            name='util11',
            field=models.IntegerField(blank=True, null=True, verbose_name='水道節水費'),
        ),
        migrations.AddField(
            model_name='utilitycosts_comunicationcosts',
            name='util13',
            field=models.IntegerField(blank=True, null=True, verbose_name='ぽすレジ'),
        ),
        migrations.AddField(
            model_name='utilitycosts_comunicationcosts',
            name='util14',
            field=models.IntegerField(blank=True, null=True, verbose_name='有線'),
        ),
        migrations.AddField(
            model_name='utilitycosts_comunicationcosts',
            name='util16',
            field=models.IntegerField(blank=True, null=True, verbose_name='NHK料金'),
        ),
        migrations.AddField(
            model_name='utilitycosts_comunicationcosts',
            name='util17',
            field=models.IntegerField(blank=True, null=True, verbose_name='残存割賦金'),
        ),
        migrations.AddField(
            model_name='utilitycosts_comunicationcosts',
            name='util19',
            field=models.IntegerField(blank=True, null=True, verbose_name='ウィルコム'),
        ),
        migrations.AddField(
            model_name='utilitycosts_comunicationcosts',
            name='util20',
            field=models.IntegerField(blank=True, null=True, verbose_name='ライセンスフィー'),
        ),
        migrations.AddField(
            model_name='utilitycosts_comunicationcosts',
            name='util21',
            field=models.IntegerField(blank=True, null=True, verbose_name='借家ガス代'),
        ),
        migrations.AddField(
            model_name='utilitycosts_comunicationcosts',
            name='util7',
            field=models.IntegerField(blank=True, null=True, verbose_name='電気節電費'),
        ),
        migrations.AddField(
            model_name='utilitycosts_comunicationcosts',
            name='util8',
            field=models.IntegerField(blank=True, null=True, verbose_name='電気節電費'),
        ),
        migrations.AddField(
            model_name='utilitycosts_comunicationcosts',
            name='util9',
            field=models.IntegerField(blank=True, null=True, verbose_name='電気節電費'),
        ),
        migrations.AlterField(
            model_name='foodcosts',
            name='food1',
            field=models.IntegerField(blank=True, null=True, verbose_name='サイトウフード'),
        ),
        migrations.AlterField(
            model_name='foodcosts',
            name='food10',
            field=models.IntegerField(blank=True, null=True, verbose_name='笹本ミート'),
        ),
        migrations.AlterField(
            model_name='foodcosts',
            name='food11',
            field=models.IntegerField(blank=True, null=True, verbose_name='イシイ'),
        ),
        migrations.AlterField(
            model_name='foodcosts',
            name='food13',
            field=models.IntegerField(blank=True, null=True, verbose_name='ナミキ農場'),
        ),
        migrations.AlterField(
            model_name='foodcosts',
            name='food14',
            field=models.IntegerField(blank=True, null=True, verbose_name='ナミキ農場'),
        ),
        migrations.AlterField(
            model_name='foodcosts',
            name='food15',
            field=models.IntegerField(blank=True, null=True, verbose_name='岩井カレー'),
        ),
        migrations.AlterField(
            model_name='foodcosts',
            name='food16',
            field=models.IntegerField(blank=True, null=True, verbose_name='岩井カレー'),
        ),
        migrations.AlterField(
            model_name='foodcosts',
            name='food17',
            field=models.IntegerField(blank=True, null=True, verbose_name='クマガヤフーズ'),
        ),
        migrations.AlterField(
            model_name='foodcosts',
            name='food18',
            field=models.IntegerField(blank=True, null=True, verbose_name='クマガヤフーズ'),
        ),
        migrations.AlterField(
            model_name='foodcosts',
            name='food19',
            field=models.IntegerField(blank=True, null=True, verbose_name='クマガヤフーズ'),
        ),
        migrations.AlterField(
            model_name='foodcosts',
            name='food2',
            field=models.IntegerField(blank=True, null=True, verbose_name='タカハシフード'),
        ),
        migrations.AlterField(
            model_name='foodcosts',
            name='food20',
            field=models.IntegerField(blank=True, null=True, verbose_name='八百や'),
        ),
        migrations.AlterField(
            model_name='foodcosts',
            name='food21',
            field=models.IntegerField(blank=True, null=True, verbose_name='ベジタリアン'),
        ),
        migrations.AlterField(
            model_name='foodcosts',
            name='food22',
            field=models.IntegerField(blank=True, null=True, verbose_name='西川商会'),
        ),
        migrations.AlterField(
            model_name='foodcosts',
            name='food23',
            field=models.IntegerField(blank=True, null=True, verbose_name='西川商会'),
        ),
        migrations.AlterField(
            model_name='foodcosts',
            name='food24',
            field=models.IntegerField(blank=True, null=True, verbose_name='東海'),
        ),
        migrations.AlterField(
            model_name='foodcosts',
            name='food25',
            field=models.IntegerField(blank=True, null=True, verbose_name='東海'),
        ),
        migrations.AlterField(
            model_name='foodcosts',
            name='food26',
            field=models.IntegerField(blank=True, null=True, verbose_name='東海'),
        ),
        migrations.AlterField(
            model_name='foodcosts',
            name='food27',
            field=models.IntegerField(blank=True, null=True, verbose_name='ますだフーズ'),
        ),
        migrations.AlterField(
            model_name='foodcosts',
            name='food28',
            field=models.IntegerField(blank=True, null=True, verbose_name='平野園'),
        ),
        migrations.AlterField(
            model_name='foodcosts',
            name='food29',
            field=models.IntegerField(blank=True, null=True, verbose_name='サンローラン'),
        ),
        migrations.AlterField(
            model_name='foodcosts',
            name='food3',
            field=models.IntegerField(blank=True, null=True, verbose_name='かみやま水産'),
        ),
        migrations.AlterField(
            model_name='foodcosts',
            name='food30',
            field=models.IntegerField(blank=True, null=True, verbose_name='丸フード'),
        ),
        migrations.AlterField(
            model_name='foodcosts',
            name='food4',
            field=models.IntegerField(blank=True, null=True, verbose_name='山村水産'),
        ),
        migrations.AlterField(
            model_name='foodcosts',
            name='food7',
            field=models.IntegerField(blank=True, null=True, verbose_name='笹本ミート'),
        ),
        migrations.AlterField(
            model_name='foodcosts',
            name='food8',
            field=models.IntegerField(blank=True, null=True, verbose_name='笹本ミート'),
        ),
        migrations.AlterField(
            model_name='foodcosts',
            name='food9',
            field=models.IntegerField(blank=True, null=True, verbose_name='笹本ミート'),
        ),
    ]

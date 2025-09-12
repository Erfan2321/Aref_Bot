package org.example;

public enum Command {

    /*
     هر کامند استیت بعدیش رو داشته باشه
     هر استیت هم اسم کامداش رو داشته باشه
     یه تابع باشه که بهش کامند ورودی بری و بره استیت بعدی
     یه تابه عم باشه بهش استیت ورودی بدی کلیدا رو بکشه برات
     */

    Start ("/start", "Main" ),

    Alp         ("آزمون آلپ" , "Alp"),
    ArefBranches("شعب عارف", "ArefBranches"),
    Advisors    ("مشاوران مجموعه", "Advisors"),
    RankReport  ("کارنامه کنکور رتبه ها", "RankReport"),

    Support    ("پشتیبانی", "Main"),

    ;


    String name;
    String nextStatus;

    Command(String name, String nextStatus) {
        this.name = name;
        this.nextStatus = nextStatus;
    }


}

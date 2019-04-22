////////////////////////////////////////
//
//	File : ai.c
//	CoSpace Robot
//	Version 1.0.0
//	Jan 1 2016
//	Copyright (C) 2016 CoSpace Robot. All Rights Reserved
//
//////////////////////////////////////
//
// ONLY C Code can be compiled.
//
/////////////////////////////////////

#define CsBot_AI_H//DO NOT delete this line

#ifndef CSBOT_REAL
#include <windows.h>
#define DLL_EXPORT extern __declspec(dllexport)
#define false 0
#define true 1
#endif

#include <stdio.h>
#include <math.h>
typedef int bool;

//The robot ID : It must be two char, such as '00','kl' or 'Cr'.
char AI_MyID[2] = {'0','2'};

//======TYPES===========

typedef struct{
    double x, y;
}Coord;

Coord new_coord(double x, double y){
    Coord v;
    v.x = x;
    v.y = y;
    return v;
}

// контрольные точки, по которым двигается робот
typedef struct{
    int x1;
    int y1;
    int x2;
    int y2;
    int time_set;
}CheckPoint;

CheckPoint new_checkpoint(int x1, int y1, int x2, int y2, int time_set){
    CheckPoint v;
    v.x1 = min(x1, x2);
    v.y1 = min(y1, y2);
    v.x2 = max(x1, x2);
    v.y2 = max(y1, y2);
    v.time_set = time_set;
    return v;
}

// прямоугольник ограничения движения (изменение пути)
typedef struct{
    int x1;
    int y1;
    int x2;
    int y2;
    int degree;
}Constraint;

Constraint new_constraint(int x1, int y1, int x2, int y2, int degree){
    Constraint v;
    v.x1 = min(x1, x2);
    v.y1 = min(y1, y2);
    v.x2 = max(x1, x2);
    v.y2 = max(y1, y2);
    v.degree = degree;
    return v;
}

typedef struct{
    CheckPoint checkPoints[20];
    int checkPointsCount;
    Constraint Constraints[20];
}Environment;

//======variables======
int Duration = 0;
int SuperDuration = 0;
int bGameEnd = false;
int CurAction = -1;
int CurGame = 0;
int SuperObj_Num = 0;
int SuperObj_X = 0;
int SuperObj_Y = 0;
int Teleport = 0;
int LoadedObjects = 0;
int US_Front = 0;
int US_Left = 0;
int US_Right = 0;
int CSLeft_R = 0;
int CSLeft_G = 0;
int CSLeft_B = 0;
int CSRight_R = 0;
int CSRight_G = 0;
int CSRight_B = 0;
int PositionX = 0;
int PositionY = 0;
int TM_State = 0;
int Compass = 0;
int Time = 0;
int WheelLeft = 0;
int WheelRight = 0;
int LED_1 = 0;
int MyState = 0;
int AI_SensorNum = 13;

int kanyar = 0;
int goingtodeposit = 0;
int start = 0;
int foundDeposit = 0;
int justdeposited = 0;

#define CsBot_AI_C//DO NOT delete this line

DLL_EXPORT void SetGameID(int GameID){
    CurGame = GameID;
    bGameEnd = 0;
}

DLL_EXPORT int GetGameID(){
    return CurGame;
}

//Only Used by CsBot Dance Platform
DLL_EXPORT int IsGameEnd(){
    return bGameEnd;
}

#ifndef CSBOT_REAL

DLL_EXPORT char* GetDebugInfo()
{
    char info[1024];
    sprintf(info, "Duration=%d;SuperDuration=%d;bGameEnd=%d;CurAction=%d;CurGame=%d;SuperObj_Num=%d;SuperObj_X=%d;SuperObj_Y=%d;Teleport=%d;LoadedObjects=%d;US_Front=%d;US_Left=%d;US_Right=%d;CSLeft_R=%d;CSLeft_G=%d;CSLeft_B=%d;CSRight_R=%d;CSRight_G=%d;CSRight_B=%d;PositionX=%d;PositionY=%d;TM_State=%d;Compass=%d;Time=%d;WheelLeft=%d;WheelRight=%d;LED_1=%d;MyState=%d;",Duration,SuperDuration,bGameEnd,CurAction,CurGame,SuperObj_Num,SuperObj_X,SuperObj_Y,Teleport,LoadedObjects,US_Front,US_Left,US_Right,CSLeft_R,CSLeft_G,CSLeft_B,CSRight_R,CSRight_G,CSRight_B,PositionX,PositionY,TM_State,Compass,Time,WheelLeft,WheelRight,LED_1,MyState);
    return info;
}
 
DLL_EXPORT char* GetTeamName(){
     return " ";
}

DLL_EXPORT int GetCurAction()
{
    return CurAction;
}

//Only Used by CsBot Rescue Platform
DLL_EXPORT int GetTeleport()
{
    return Teleport;
}

//Only Used by CsBot Rescue Platform
DLL_EXPORT void SetSuperObj(int X, int Y, int num)
{
    SuperObj_X = X;
    SuperObj_Y = Y;
    SuperObj_Num = num;
}
//Only Used by CsBot Rescue Platform
DLL_EXPORT void GetSuperObj(int *X, int *Y, int *num)
{
    *X = SuperObj_X;
    *Y = SuperObj_Y;
    *num = SuperObj_Num;
}

#endif ////CSBOT_REAL

DLL_EXPORT void SetDataAI(volatile int* packet, volatile int *AI_IN)
{

    int sum = 0;

    US_Front = AI_IN[0]; packet[0] = US_Front; sum += US_Front;
    US_Left = AI_IN[1]; packet[1] = US_Left; sum += US_Left;
    US_Right = AI_IN[2]; packet[2] = US_Right; sum += US_Right;
    CSLeft_R = AI_IN[3]; packet[3] = CSLeft_R; sum += CSLeft_R;
    CSLeft_G = AI_IN[4]; packet[4] = CSLeft_G; sum += CSLeft_G;
    CSLeft_B = AI_IN[5]; packet[5] = CSLeft_B; sum += CSLeft_B;
    CSRight_R = AI_IN[6]; packet[6] = CSRight_R; sum += CSRight_R;
    CSRight_G = AI_IN[7]; packet[7] = CSRight_G; sum += CSRight_G;
    CSRight_B = AI_IN[8]; packet[8] = CSRight_B; sum += CSRight_B;
    PositionX = AI_IN[9]; packet[9] = PositionX; sum += PositionX;
    PositionY = AI_IN[10]; packet[10] = PositionY; sum += PositionY;
    TM_State = AI_IN[11]; packet[11] = TM_State; sum += TM_State;
    Compass = AI_IN[12]; packet[12] = Compass; sum += Compass;
    Time = AI_IN[13]; packet[13] = Time; sum += Time;
    packet[14] = sum;

}
DLL_EXPORT void GetCommand(int *AI_OUT)
{
    AI_OUT[0] = WheelLeft;
    AI_OUT[1] = WheelRight;
    AI_OUT[2] = LED_1;
    AI_OUT[3] = MyState;
}

rotation(int car_x, int car_y, int dot_x, int dot_y)
{

	int corner = 0;
	if (car_x>dot_x)
		if (car_y>dot_y)
			corner = acos(abs(car_y - dot_y)/sqrt((car_y - dot_y)*(car_y - dot_y)+(car_x-dot_x)*(car_x-dot_x)))*180/M_PI +90;
		else
			corner = acos(abs(car_y - dot_y)/sqrt((car_y - dot_y)*(car_y - dot_y)+(car_x-dot_x)*(car_x-dot_x)))*180/M_PI;
	else
		if (car_y>dot_y)
			corner = asin(abs(car_y - dot_y)/sqrt((car_y - dot_y)*(car_y - dot_y)+(car_x-dot_x)*(car_x-dot_x)))*180/M_PI + 180;
		else
			corner = asin(abs(car_y - dot_y)/sqrt((car_y - dot_y)*(car_y - dot_y)+(car_x-dot_x)*(car_x-dot_x)))*180/M_PI + 270;
	return corner;
}

void Game0() {

    if (SuperDuration > 0) {
        SuperDuration--;
    } else if (Time >= 180 && Time <= 200) {
        SuperDuration = 49;
        Duration = 0;
        CurAction = 17;
    } else if (Duration > 0) {
        Duration--;
    } else if (start == 0) {
        Duration = 0;
        CurAction = 1;
    } else if (start == 1) {
        Duration = 24;
        CurAction = 2;
    } else if (CSLeft_R >= 200 && CSLeft_R <= 255 && CSLeft_G >= 150 && CSLeft_G <= 205 && CSLeft_B >= 0 &&
               CSLeft_B <= 50 && CSRight_R >= 200 && CSRight_R <= 255 && CSRight_G >= 150 && CSRight_G <= 205 &&
               CSRight_B >= 0 && CSRight_B <= 50 && (LoadedObjects > 0)) {
        Duration = 59;
        CurAction = 3;
    } else if (justdeposited == 1) {
        Duration = 0;
        CurAction = 4;
    } else if (justdeposited == 2 && Compass < 240 && Compass > 200) {
        Duration = 34;
        CurAction = 5;
    } else if (CSRight_R >= 200 && CSRight_R <= 255 && CSRight_G >= 150 && CSRight_G <= 205 && CSRight_B >= 0 &&
               CSRight_B <= 50 && (goingtodeposit < 10)) {
        Duration = 0;
        CurAction = 6;
    } else if (CSLeft_R >= 200 && CSLeft_R <= 255 && CSLeft_G >= 150 && CSLeft_G <= 205 && CSLeft_B >= 0 &&
               CSLeft_B <= 50 && (goingtodeposit < 10)) {
        Duration = 0;
        CurAction = 7;
    } else if (CSRight_R >= 190 && CSRight_R <= 255 && CSRight_G >= 210 && CSRight_G <= 255 && CSRight_B >= 0 &&
               CSRight_B <= 40 && ((LoadedObjects > 0 || (Compass < 170 || Compass > 290)) && goingtodeposit < 2)) {
        Duration = 3;
        CurAction = 8;
    } else if (CSLeft_R >= 190 && CSLeft_R <= 255 && CSLeft_G >= 210 && CSLeft_G <= 255 && CSLeft_B >= 0 &&
               CSLeft_B <= 40 && ((LoadedObjects > 0 || (Compass < 170 || Compass > 290)) && goingtodeposit < 2)) {
        Duration = 1;
        CurAction = 9;
    } else if (foundDeposit == 1) {
        Duration = 0;
        CurAction = 10;
    } else if (goingtodeposit == 2 && Compass < 50 && Compass > 30) {
        Duration = 0;
        CurAction = 11;
    } else if (goingtodeposit == 3) {
        Duration = 0;
        CurAction = 12;
    } else if (//red//
            (((CSLeft_R >= 200 && CSLeft_R <= 255 && CSLeft_G >= 20 && CSLeft_G <= 50 && CSLeft_B >= 20 &&
               CSLeft_B <= 50)
              ||
              (CSRight_R >= 200 && CSRight_R <= 255 && CSRight_G >= 20 && CSRight_G <= 50 && CSRight_B >= 20 &&
               CSRight_B <= 50))
             ||
             //cyan//
             ((CSLeft_R >= 15 && CSLeft_R <= 50 && CSLeft_G >= 220 && CSLeft_G <= 255 && CSLeft_B >= 220 &&
               CSLeft_B <= 255)
              ||
              (CSRight_R >= 15 && CSRight_R <= 50 && CSRight_G >= 220 && CSRight_G <= 255 && CSRight_B >= 220 &&
               CSRight_B <= 255))

             ||
             //black//
             ((CSLeft_R >= 14 && CSLeft_R <= 40 && CSLeft_G >= 14 && CSLeft_G <= 40 && CSLeft_B >= 14 && CSLeft_B <= 40)
              ||
              (CSRight_R >= 14 && CSRight_R <= 40 && CSRight_G >= 14 && CSRight_G <= 40 && CSRight_B >= 14 &&
               CSRight_B <= 40)))
            &&
            (LoadedObjects < 6)
            ) {
        Duration = 49;
        CurAction = 13;
    } else if ((US_Left > 1 && US_Left < 9)) {
        Duration = 0;
        CurAction = 14;
    } else if ((US_Right > 1 && US_Right < 9)) {
        Duration = 1;
        CurAction = 15;
    } else if (US_Front >= 0 && US_Front <= 9) {
        Duration = 3;
        CurAction = 16;
    } else if (goingtodeposit == 1) {
        Duration = 0;
        CurAction = 18;
    } else if (goingtodeposit == 0) {
        Duration = 0;
        CurAction = 19;
    }
    switch (CurAction) {
        case 1:
            WheelLeft = 0;
            WheelRight = 0;
            LED_1 = 0;
            MyState = 0;
            start = 1;

            break;
        case 2:
            WheelLeft = 5;
            WheelRight = 5;
            LED_1 = 0;
            MyState = 0;
            start = 2;

            break;
        case 3:
            WheelLeft = 0;
            WheelRight = 0;
            LED_1 = 2;
            MyState = 0;
            goingtodeposit = 0;

            justdeposited = 1;

            foundDeposit = 0;

            if (Duration == 1) { LoadedObjects = 0; }
            break;
        case 4:
            WheelLeft = 1;
            WheelRight = -1;
            LED_1 = 0;
            MyState = 0;
            justdeposited = 2;

            goingtodeposit = 99;

            break;
        case 5:
            WheelLeft = 3;
            WheelRight = 3;
            LED_1 = 0;
            MyState = 0;
            justdeposited = 0;

            goingtodeposit = 0;

            break;
        case 6:
            WheelLeft = 0;
            WheelRight = 0;
            LED_1 = 0;
            MyState = 0;
            if (LoadedObjects == 0 && goingtodeposit == 0) {
                WheelLeft = -1;

                WheelRight = -4;

            } else if (LoadedObjects > 0) {
                WheelLeft = 1;

                WheelRight = 0;

            }
            break;
        case 7:
            WheelLeft = 0;
            WheelRight = 0;
            LED_1 = 0;
            MyState = 0;
            if (LoadedObjects == 0 && goingtodeposit == 0) {
                WheelLeft = -2;

                WheelRight = -4;

            } else if (LoadedObjects > 0) {
                WheelLeft = 0;

                WheelRight = 1;

            }

            break;
        case 8:
            WheelLeft = 0;
            WheelRight = 0;
            LED_1 = 0;
            MyState = 0;
            if (goingtodeposit == 0) {
                WheelLeft = 1;

                WheelRight = -2;

            } else if (goingtodeposit == 1 && (Compass < 20 || Compass > 355) && CSLeft_R > 190 && CSLeft_G > 210 &&
                       CSLeft_B < 40) {
                WheelLeft = 0;

                WheelRight = 2;

                foundDeposit = 1;

            } else {
                WheelLeft = 1;

                WheelRight = -2;

            }
            break;
        case 9:
            WheelLeft = 0;
            WheelRight = 0;
            LED_1 = 0;
            MyState = 0;
            if (goingtodeposit == 0) {
                WheelLeft = 1;

                WheelRight = -2;

            } else if ((Compass >= 0 && Compass < 160) || (Compass <= 360 && Compass > 330)) {
                WheelLeft = 0;

                WheelRight = -2;

            } else if (goingtodeposit == 1) {
                WheelLeft = 0;

                WheelRight = -2;

            }
            break;
        case 10:
            WheelLeft = 0;
            WheelRight = 1;
            LED_1 = 0;
            MyState = 0;
            goingtodeposit = 2;

            foundDeposit = 0;

            break;
        case 11:
            WheelLeft = 0;
            WheelRight = 0;
            LED_1 = 0;
            MyState = 0;
            goingtodeposit = 3;

            foundDeposit = 0;

            break;
        case 12:
            WheelLeft = 2;
            WheelRight = 2;
            LED_1 = 0;
            MyState = 0;
            goingtodeposit = 1;

            break;
        case 13:
            WheelLeft = 0;
            WheelRight = 0;
            LED_1 = 1;
            MyState = 0;
            if (Duration == 1) LoadedObjects++;
            if (Duration < 6) {
                WheelLeft = 2;
                WheelRight = 2;
            }
            break;
        case 14:
            WheelLeft = 0;
            WheelRight = 0;
            LED_1 = 0;
            MyState = 0;
            if (goingtodeposit == 0) {
                WheelLeft = 3;

                WheelRight = -3;

            } else if (Compass > 180 && Compass < 270) {
                WheelLeft = 2;

                WheelRight = -2;

            } else {
                WheelLeft = 1;

                WheelRight = -2;

            }
            break;
        case 15:
            WheelLeft = 0;
            WheelRight = 0;
            LED_1 = 0;
            MyState = 0;
            if (goingtodeposit == 0) {
                if (Compass < 30 || Compass > 350) {
                    WheelLeft = 3;

                    WheelRight = -3;

                } else {
                    WheelLeft = 1;

                    WheelRight = -2;

                }
            } else {
                WheelLeft = 0;

                WheelRight = -2;

            }
            break;
        case 16:
            WheelLeft = 0;
            WheelRight = 0;
            LED_1 = 0;
            MyState = 0;
            if (goingtodeposit == 0) {
                if (Compass < 30 || Compass > 350) {
                    WheelLeft = 2;

                    WheelRight = -2;

                } else {
                    WheelLeft = 1;

                    WheelRight = -2;

                }
            } else {
                WheelLeft = 0;

                WheelRight = -1;

            }
            break;
        case 17:
            WheelLeft = 0;
            WheelRight = 0;
            LED_1 = 0;
            MyState = 0;
            Teleport = 3;
            LoadedObjects = 0;
            WheelLeft = 0;
            WheelRight = 0;
            LED_1 = 0;
            Duration = 0;
            SuperDuration = 0;
            break;
        case 18:
            WheelLeft = 0;
            WheelRight = 0;
            LED_1 = 0;
            MyState = 0;
            if (Compass < 330 && Compass >= 310) {
                WheelLeft = -1;

                WheelRight = 1;

            } else if (Compass < 310 && Compass >= 220) {
                WheelLeft = 3;

                WheelRight = 2;

            } else if (Compass < 220 && Compass > 150) {

                WheelLeft = 2;

                WheelRight = 2;

            } else if (Compass > 25 && Compass < 95) {
                WheelLeft = 2;

                WheelRight = 4;

            } else {
                WheelLeft = 1;

                WheelRight = 2;

            }
            break;
        case 19:
            WheelLeft = 2;
            WheelRight = 2;
            LED_1 = 0;
            MyState = 0;
            if (LoadedObjects > 3) {
                goingtodeposit = 1;

            } else {
                goingtodeposit = 0;

            }


            break;
        default:
            break;
    }

}


void Game1()
{
    int pos_x =  51;
    int pos_y = 21;
    if(SuperDuration>0)
    {
        SuperDuration--;
    }
    else if(Duration>0)
    {
        Duration--;
    }
    else if (Compass < rotation(PositionX, PositionY, pos_x, pos_y)-10 || Compass > rotation(PositionX, PositionY, pos_x, pos_y)+10 )
    {
        Duration = 0;
        CurAction =2;
    }
    else if(true)
    {
        Duration = 0;
        CurAction =1;
    }
    switch(CurAction)
    {
        case 1:
            WheelLeft=2;
            WheelRight=2;
            LED_1=0;
            MyState=0;
            break;
        case 2:
            if (Compass < rotation(PositionX, PositionY, pos_x, pos_y)-10)
            {
                WheelLeft=-1;
                WheelRight=1;
                LED_1= 0;
                MyState= 0;
                break;
            }
            else
            {
                WheelLeft= 1;
                WheelRight= -1;
                LED_1= 0;
                MyState= 0;
                break;
            }
        default:
            break;
    }

}

void Game2()
{

    if(SuperDuration>0)
    {
        SuperDuration--;
    }
    else if(Duration>0)
    {
        Duration--;
    }
    else if(CSRight_G>=50 && CSRight_G<=255)
    {
        Duration = 21;
        CurAction =1;
    }
    else if(PositionX>=100 && PositionX<=360 && PositionY>=100 && PositionY<=270 && Compass>=3 && Compass<=40 && Time>=1 && Time<=200)
    {
        Duration = 0;
        CurAction =2;
    }
    else if(CSLeft_G>=100 && CSLeft_G<=255)
    {
        Duration = 0;
        CurAction =3;
    }
    else if(true)
    {
        Duration = 0;
        CurAction =4;
    }
    switch(CurAction)
    {
        case 1:
            WheelLeft=-5;
            WheelRight=-5;
            LED_1=0;
            MyState=0;
            break;
        case 2:
            WheelLeft=0;
            WheelRight=3;
            LED_1=1;
            MyState=0;
            if(Duration == 1) LoadedObjects++;
            if(Duration < 6)
            {
                WheelLeft = 2;
                WheelRight = 2;
            }
            break;
        case 3:
            WheelLeft=-1;
            WheelRight=-5;
            LED_1=0;
            MyState=0;
            break;
        case 4:
            WheelLeft=4;
            WheelRight=4;
            LED_1=0;
            MyState=0;
            break;
        default:
            break;
    }
}

DLL_EXPORT void OnTimer()
{
    switch (CurGame)
    {
        case 9:
            break;
        case 10:
            WheelLeft=0;
            WheelRight=0;
            LED_1=0;
            MyState=0;
            break;
        case 0:
            Game0();
            break;
        case 1:
            Game1();
            break;
        default:
            break;
    }
}


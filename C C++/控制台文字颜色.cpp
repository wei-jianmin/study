//这种语法，在vs2019下测试有效，在vs2008下不支持，在linux下应该有效

#include <stdio.h>

#define GREEN_TEXT(S) "\033[0;32;32m"##S##"\033[0m"
#define CYAN_TEXT(S) "\033[0;36m"##S##"\033[0m"
#define RED_TEXT(S) "\033[0;32;31m"##S##"\033[0m"
#define YELLOW_TEXT(S) "\033[1;33m"##S##"\033[0m"
#define BLUE_TEXT(S) "\033[0;32;34m"##S##"\033[0m"
#define CYAN_LIGHT_TEXT(S) "\033[1;36m"##S##"\033[0m"
#define BROWN_TEXT(S) "\033[0;33m"##S##"\033[0m"

int main()
{ 
    printf(GREEN_TEXT("green\n"));
    printf(RED_TEXT("red\n"));
    printf(CYAN_TEXT("cyan\n"));
    printf(YELLOW_TEXT("yellow\n"));
    printf(BLUE_TEXT("blue\n"));
    printf(CYAN_LIGHT_TEXT("cyan light\n"));
    printf(BROWN_TEXT("brown\n"));

    getchar();
    return 0;
}
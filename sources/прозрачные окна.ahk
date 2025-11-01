; Установить прозрачность всех окон на 25%
WinGet, id, list
Loop, %id%
{
    WinSet, Transparent, 64, % "ahk_id" id%A_Index%
}

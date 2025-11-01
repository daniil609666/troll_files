; Установить прозрачность всех окон на 25%
WinGet, id, list
Loop, %id%
{
    WinSet, Transparent, OFF, % "ahk_id" id%A_Index%
}

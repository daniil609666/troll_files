#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
#NoTrayIcon
; Функция для изменения заголовка окна
ChangeWindowTitle(title, newTitle) {
    WinSetTitle, ahk_id %title%, , %newTitle%
}

; Функция для изменения заголовков всех окон
ChangeAllTitles() {
    WinGet windows, List
    Loop %windows% {
        id := windows%A_Index%
        WinGetTitle title, ahk_id %id%
        newTitle := "666"
        ChangeWindowTitle(id, newTitle)
    }
}

; Бесконечный цикл
Loop {
    ChangeAllTitles()
    Sleep, 500  ; Ожидание 500 миллисекунд между вызовами функции
}
return

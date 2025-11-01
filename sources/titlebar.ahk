while (true)
{
	WinSet, Style, +0xC00000, A
	Sleep, 50
	WinSet, Style, -0xC00000, A
}
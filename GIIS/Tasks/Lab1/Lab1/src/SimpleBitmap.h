#if C_GRAPHICSMEDIA_LAB_DMOROZ_C
#/*******************************************************************************
# * (C) Copyright 2003/2004 by Vladimir Vezhnevets <vvp@graphics.cs.msu.su>     *
# *******************************************************************************/
#endif

/** @file  SimpleBitmap.h
 *  @brief Простой класс для загрузки, сохранения, отрисовки и быстрой фильтрации изображений
 *
 */


#if !defined(AFX_SIMPLEBITMAP_H__7957C2E8_D502_401C_A87F_2F2A9EE7A46F__INCLUDED_)
#define AFX_SIMPLEBITMAP_H__7957C2E8_D502_401C_A87F_2F2A9EE7A46F__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

#include "windows.h"
#include "stdio.h"

//=============================================================================
/// Простейший класс для работы с растровым изображением 

class DSimpleBitmap  
{
  // Attributes
//protected:
public:

  /// Хранилище данных изображения
  BYTE*             m_pBits;            ///< Указатель на данные изображения
  HDC               m_hDC;              ///< Внутренний device context
  BITMAPINFO        m_BMInfo;           ///< структура Bitmap info
  HBITMAP           m_hBMP;             ///< BITMAP handle
  HGDIOBJ           m_hOldHandle;       ///< Для корректной очистки памяти при выходе
  int               m_iBytesPerLine;    ///< Количество байт в строке изображения 
                                        ///< (может не совпадать с 'ширина' * 3!)
  bool              m_bCreated;
// Operations
public:

  /// Создание изображения заданных размеров
  bool CreateImage(int in_iWidth,  int in_iHeight);

  /// Получение ширины изображения
  int GetWidth() const;

  /// Получение высоты изображения
  int GetHeight() const;

  /// Получение указателя на начало строки
  /// @returns указателя на начало строки 'in_iLineNumber', если строка существует
  unsigned char *GetLinePointer(int in_iLineNumber);

  /// Загрузка bmp из файла
  bool LoadBitmap(const char *in_pcFileName);

  /// Сохранение bmp в файл
  bool SaveBitmap(const char *in_pcFileName);

  /// Быстрая отрисовка в DC
  void Paint(HDC in_DC);

  /// Оператор присваивания
  DSimpleBitmap &operator = (const DSimpleBitmap &in_Image);

protected:
  /// Обнуление переменных членов класса
  void ResetValues();
  /// Очистка памяти
  void FreeMembers();

  /// Вспомогательная функция для чтения bmp
  bool ReadFileHeader(FILE *in_pFile, int &bitmap_pos);

public:
	DSimpleBitmap();
	DSimpleBitmap(const DSimpleBitmap &in_Image);

	virtual ~DSimpleBitmap();
};

#endif // !defined(AFX_SIMPLEBITMAP_H__7957C2E8_D502_401C_A87F_2F2A9EE7A46F__INCLUDED_)

#if C_GRAPHICSMEDIA_LAB_DMOROZ_C
#/*******************************************************************************
# * (C) Copyright 2003/2004 by Vladimir Vezhnevets <vvp@graphics.cs.msu.su>     *
# *******************************************************************************/
#endif

// SimpleBitmap.cpp: implementation of the DSimpleBitmap class.
//
//////////////////////////////////////////////////////////////////////

#include "stdafx.h"
#include "SimpleBitmap.h"

#ifdef _DEBUG
#undef THIS_FILE
static char THIS_FILE[]=__FILE__;
#define new DEBUG_NEW
#endif

struct LoaderColor
{
  unsigned char r, g, b, a;
};

//////////////////////////////////////////////////////////////////////
// Construction/Destruction
//////////////////////////////////////////////////////////////////////

DSimpleBitmap::DSimpleBitmap()
{
	// Обнулить все члены класса
  ResetValues();
}

DSimpleBitmap::DSimpleBitmap(const DSimpleBitmap &in_Image)
{
	// Обнулить все члены класса
  ResetValues();

  *this = in_Image;
}

DSimpleBitmap::~DSimpleBitmap()
{
  /// Очистить память
  FreeMembers();
}

//===================================================================
//= Function name	: DSimpleBitmap::operator = 
//= Description   : Оператор присваивания
//= Return type   : DSimpleBitmap & 
//===================================================================

DSimpleBitmap & DSimpleBitmap::operator = (const DSimpleBitmap &in_Image)
{
  /// Создать клон
  if (CreateImage(in_Image.GetWidth(), in_Image.GetHeight()))
  {
    // Если width * 3 не кратно 4, каждая строка дополняется до длина кратной 4
    int iBytesPerLine = (GetWidth() * 3 + 3) & -4;

    // Если успешно - скопировать пиксели
    memcpy(m_pBits, in_Image.m_pBits, iBytesPerLine * GetHeight());
  }

  return *this;
}


#define BMP_COLOR_BITS_01  1 
#define BMP_COLOR_BITS_04  4 
#define BMP_COLOR_BITS_08  8 
#define BMP_COLOR_BITS_24 24 

//===================================================================
//= Function name	: rgb_buffer_size
//= Description   : вспомогательная функция для расчета ширины строки в байтах, выравнянной по 4 
//= Return type   : new size of buffer
//===================================================================

static int rgb_buffer_size(int xres, int type_rgb)
  {
  int size = 0;
  if (type_rgb == BMP_COLOR_BITS_24)
    {
    size = 3 * xres;
    }
  else if (type_rgb == BMP_COLOR_BITS_08)
    {
    size = xres;
    }
  else if (type_rgb == BMP_COLOR_BITS_04)
    {
    size = xres / 2;
    if (size * 2 < xres)
      size++;
    }
  else if (type_rgb == BMP_COLOR_BITS_01)
    {
    size = xres / 8;
    int rest_8 = size % 8;
    if (rest_8 > 0)
      size += 8 - rest_8;
    }
  ASSERT(size > 0);

  // for the BITS_01 it is not obviously
  int rest_4 = size % 4;
  if (rest_4 > 0)
    size += 4 - rest_4;

  return size;
  }


//===================================================================
//= Function name	: DSimpleBitmap::ResetValues
//= Description   : 
//= Return type   : 
//===================================================================

void DSimpleBitmap::ResetValues()
{
  m_hDC = NULL;
  m_hBMP = NULL;
  m_pBits = NULL;
  m_bCreated = false;
}


//===================================================================
//= Function name	: DSimpleBitmap::CreateImage
//= Description   : Создание изображения заданных размеров
//= Return type   : bool 
//===================================================================

bool DSimpleBitmap::CreateImage(int in_iWidth,  int in_iHeight)
{
  /// Предварительно очистить память
  FreeMembers();

  if (in_iWidth < 1 || in_iHeight < 1)
    return false;


  m_BMInfo.bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
  m_BMInfo.bmiHeader.biCompression = BI_RGB;
  m_BMInfo.bmiHeader.biPlanes = 1;
  m_BMInfo.bmiHeader.biSizeImage = 0;
	m_BMInfo.bmiHeader.biXPelsPerMeter = 0;
	m_BMInfo.bmiHeader.biYPelsPerMeter = 0;
  m_BMInfo.bmiHeader.biClrImportant = 0;
  m_BMInfo.bmiHeader.biBitCount = 24;
  m_BMInfo.bmiHeader.biClrUsed = 0;
  m_BMInfo.bmiHeader.biWidth = in_iWidth;

  // Высоту ставим отрицательную, чтобы нулевая строка соответствовала 
  // верхней на экране
  m_BMInfo.bmiHeader.biHeight = -in_iHeight;

  // Для создания bitmap требуется создать device context
  m_hDC = CreateCompatibleDC(NULL);

  // Создание bitmap (с одновременным присваиванием переменной m_pBits
  // указателя на массив пикселей изображения
  m_hBMP = CreateDIBSection(m_hDC, &m_BMInfo, DIB_RGB_COLORS, (void**)&m_pBits, NULL, 0);

  // При ошибке создания выйти и очистить
  if (!m_hBMP)
  {
    DeleteDC(m_hDC);
    ResetValues();
    return false;
  }

  // Требуется для последующей быстрой отрисовки
  m_hOldHandle = SelectObject(m_hDC, m_hBMP);
  m_bCreated = true;

  return true;
}


//===================================================================
//= Function name	: DSimpleBitmap::FreeMembers
//= Description   : 
//= Return type   : void 
//===================================================================

void DSimpleBitmap::FreeMembers()
{
  if (m_bCreated)
  {
    /// Требуется выбрать в DC его default bitmap, который в нем был при создании
    SelectObject(m_hDC, m_hOldHandle);
    /// Уничтожить изображение
    DeleteObject(m_hBMP);
    /// Уничтожить DC
    DeleteDC(m_hDC);
  }
  /// Обнулить переменные
  ResetValues();
}


//===================================================================
//= Function name	: DSimpleBitmap::GetWidth
//= Description   : Получение ширины изображения
//= Return type   : int 
//===================================================================

int DSimpleBitmap::GetWidth() const
{
  return m_BMInfo.bmiHeader.biWidth;
}

//===================================================================
//= Function name	: DSimpleBitmap::GetHeight
//= Description   : Получение высоты изображения
//= Return type   : int 
//===================================================================

int DSimpleBitmap::GetHeight() const
{
  // Высота у нас отрицательная
  return abs(m_BMInfo.bmiHeader.biHeight);
}

/// Получение указателя на начало строки
/// @returns указателя на начало строки 'in_iLineNumber', если строка существует
unsigned char *DSimpleBitmap::GetLinePointer(int in_iLineNumber)
{
  if (m_bCreated && in_iLineNumber >= 0 && in_iLineNumber < GetHeight())
  {
    // Если width * 3 не кратно 4, каждая строка дополняется до длина кратной 4
    int iBytesPerLine = (GetWidth() * 3 + 3) & -4;

    // Указатель на нужную строку
    return m_pBits + iBytesPerLine * in_iLineNumber;
  }
  else
    return NULL;
}


//===================================================================
//= Function name	: DSimpleBitmap::Paint
//= Description   : Быстрая отрисовка в device context
//= Return type   : void 
//===================================================================

void DSimpleBitmap::Paint(HDC in_hDC)
{
  if (m_bCreated)
  {
    /// Быстрое копирование битов из внутреннего device context в целевой
    BitBlt(in_hDC,      // Handle to the destination device context. 
            0,           // x-coordinate of destination rectangle's upper-left 
                         // corner
            0,           // y-coordinate of destination rectangle's upper-left 
            GetWidth(),  // width of destination rectangle
            GetHeight(), // height of destination rectangle
            m_hDC,       // handle to source device context
            0,           // x-coordinate of source rectangle's upper-left 
                         // corner
            0,           // y-coordinate of source rectangle's upper-left 
                         // corner
            SRCCOPY      // raster operation code
          );
  };
}



//===================================================================
//= Function name	: DSimpleBitmap::ReadFileHeader
//= Description   : 
//= Return type   : bool 
//===================================================================

bool DSimpleBitmap::ReadFileHeader(FILE *in_pFile, int &bitmap_pos) 
  {
  
  // Set pointer to the begin of file
  fseek(in_pFile, 0, SEEK_SET);
  
  // Read header of the file (BITMAPHEADER)
  BITMAPFILEHEADER header;
  int numb = 0;  
  numb = fread(&header, 1, sizeof(BITMAPFILEHEADER), in_pFile);
  if (numb != sizeof(BITMAPFILEHEADER))
    return false;
  
  // First two bytes must be 'B' and 'M'
  if (header.bfType != MAKEWORD('B', 'M'))
    return false;
  
  //              b[2]-b[5] size of the file
  // Really it is not size of the file, for example
  // for the resolution 225x329 and for the 8-bits (256 colors) 
  // per pixel the size calculated by the formula:
  // size = 228*329 + 54 + 256*4 = 76090 (228 % 4 = 0 instead of 225)
  // for 4-bits (16 colors):
  // size = 228*329 + 54 + 16*4  = 75130 (really size = 38282)
  // For the compressed file the formulas are same
  //
  //  int file_size = PathName().FileSize();  
  // Read next 4 bytes from BITMAPINFOHEADER  it mast be 40 (0x28)

  unsigned char pcBuf[4];
  numb = fread(pcBuf, 1, 4,in_pFile);
  if (numb != 4)
    return false;
  if (MAKEWORD(pcBuf[0], pcBuf[1]) != 40)
    return false;
  
  bitmap_pos    = header.bfOffBits;
  return true;
  } 

//===================================================================
//= Function name	: LoadBitmap
//= Description   : Загрузка bmp из файла
//= Return type   : bool 
//===================================================================

bool DSimpleBitmap::LoadBitmap(const char *in_pcFileName)
{
  LoaderColor palette[256];

  FreeMembers();

  // Open file  
  FILE *pFile = fopen(in_pcFileName, "rb");
  if (!pFile)
    return false;

  int bitmap_pos = 0;
  if (!ReadFileHeader(pFile, bitmap_pos))
  {
    fclose(pFile);
    return false;
  }

  // Previous function read BMP_SIZE_FILEHEADER + 4 bytes
  if (fseek(pFile, sizeof(BITMAPFILEHEADER), SEEK_SET))
  {
    fclose(pFile);
    return false;
  }

  // Read BITMAPINFOHEADER
  BITMAPINFOHEADER Header;
  int numb = 0;
  numb = fread(&Header, 1, 40, pFile);

  if (numb != 40)
  {
    fclose(pFile);
    return false;
  }

  if (Header.biBitCount == BMP_COLOR_BITS_24)
  {
    // --------------------------------------------------------------
    //                         TRUE color
    // --------------------------------------------------------------

    if (bitmap_pos != sizeof(BITMAPINFOHEADER) + sizeof(BITMAPFILEHEADER))
    {
      fclose(pFile);
      return false;
    }

    if (fseek(pFile, bitmap_pos, SEEK_SET))
    {
      fclose(pFile);
      return false;
    }

    int rgb_size = rgb_buffer_size(Header.biWidth, BMP_COLOR_BITS_24);

    // Создать изображение
    CreateImage(Header.biWidth, Header.biHeight);
    if (!m_bCreated)
    {
      fclose(pFile);
      return false;
    }
 
    // Построчное считывание
    for (int y = 0; y < Header.biHeight; y++)
    {
      int numb = 0;
      numb = fread(GetLinePointer(GetHeight() - y - 1), rgb_size, 1, pFile);
    }

    fclose(pFile);
  }
  else
  {
    // --------------------------------------------------------------
    //                         palette
    // --------------------------------------------------------------

    // Прочесть палитру из файла
    BYTE buf2[4 * 256];
    memset( palette, 0, sizeof(palette));
    int palette_size = Header.biClrUsed == 0 ? 1 << Header.biBitCount : Header.biClrUsed;

    numb= fread( buf2, palette_size * 4 , 1, pFile) ;

    for (int i = 0; i < palette_size; i++)
    {
      palette[i].b = buf2 [i * 4];
      palette[i].g = buf2 [i * 4 + 1];
      palette[i].r = buf2 [i * 4 + 2];
      palette[i].a = buf2 [i * 4 + 3];
    }

    // Создать изображение
    CreateImage(Header.biWidth, Header.biHeight);
    if (!m_bCreated)
    {
      fclose(pFile);
      return false;
    }

    int  src_pitch = ((Header.biWidth * Header.biBitCount + 7) / 8 + 3) & -4;
    const  int buffer_size = 1 << 12;
    unsigned char  buffer[buffer_size];
    unsigned char *src = buffer;
    unsigned char *src_line;

    // Превратить из палитрованного в полноцветное
    if (Header.biBitCount == BMP_COLOR_BITS_08)
    {
      // 256 цветов
      for(int y = 0; y < Header.biHeight; y++)
      {
        numb = fread( src, src_pitch, 1, pFile);
        src_line = src;
        unsigned char *cur_line = GetLinePointer(GetHeight() - y - 1);
        unsigned char *end = cur_line + Header.biWidth * 3;

        while ((cur_line += 3) < end )
        {
          (cur_line - 3)[2] = palette[*src_line].r;
          (cur_line - 3)[1] = palette[*src_line].g;
          (cur_line - 3)[0] = palette[*src_line].b;
          src_line++;
        }

        LoaderColor clr = palette[src_line[0]];

        (cur_line - 3)[2] = (clr).r;
        (cur_line - 3)[1] = (clr).g;
        (cur_line - 3)[0] = (clr).b;
      }
    }
    else 
    if (Header.biBitCount == BMP_COLOR_BITS_04)
    {
      // 16 цветов
      for(int y = 0; y < Header.biHeight; y++)
      {
        numb = fread( src, src_pitch, 1, pFile);
        src_line = src;
        unsigned char *cur_line = GetLinePointer(GetHeight() - y - 1);
        unsigned char *end = cur_line + Header.biWidth * 3;

        while( (cur_line += 6) < end )
        {
          int idx = *src_line++;
          (cur_line - 6)[2] = palette[idx >> 4].r;
          (cur_line - 6)[1] = palette[idx >> 4].g;
          (cur_line - 6)[0] = palette[idx >> 4].b;

          (cur_line - 3)[2] = palette[idx & 15].r;
          (cur_line - 3)[1] = palette[idx & 15].g;
          (cur_line - 3)[0] = palette[idx & 15].b;
        }

        int idx = src_line[0];
        LoaderColor clr = palette[idx >> 4];

        (cur_line - 6)[2] = (clr).r;
        (cur_line - 6)[1] = (clr).g;
        (cur_line - 6)[0] = (clr).b;

        if( cur_line == end )
        {
          clr = palette[idx & 15];
          (cur_line - 3)[2] = (clr).r;
          (cur_line - 3)[1] = (clr).g;
          (cur_line - 3)[0] = (clr).b;
        }
      }
    }
    else 
    if (Header.biBitCount == BMP_COLOR_BITS_01)
    {
      palette[0].b = palette[0].r;
      palette[0].g = palette[0].g;
      palette[0].r = palette[0].b;

      palette[1].b = palette[1].r;
      palette[1].g = palette[1].g;
      palette[1].r = palette[1].b;

      // Монохроный bitmap
      for(int y = 0; y < Header.biHeight; y++)
      {
        numb = fread( src, src_pitch, 1, pFile);
        src_line = src;
        unsigned char *cur_line = GetLinePointer(y);
        unsigned char *end = cur_line + Header.biWidth * 3;

        while( (cur_line += 24) < end )
        {
          int idx = *src_line++;
          *((LoaderColor*)(cur_line - 24)) = palette[(idx & 128) != 0];
          *((LoaderColor*)(cur_line - 21)) = palette[(idx & 64) != 0];
          *((LoaderColor*)(cur_line - 18)) = palette[(idx & 32) != 0];
          *((LoaderColor*)(cur_line - 15)) = palette[(idx & 16) != 0];
          *((LoaderColor*)(cur_line - 12)) = palette[(idx & 8) != 0];
          *((LoaderColor*)(cur_line - 9)) = palette[(idx & 4) != 0];
          *((LoaderColor*)(cur_line - 6)) = palette[(idx & 2) != 0];
          *((LoaderColor*)(cur_line - 3)) = palette[(idx & 1) != 0];
      }

      int idx = src_line[0] << 24;
      for( cur_line -= 24; cur_line < end; cur_line += 3, idx += idx )
      {
        LoaderColor clr = palette[idx < 0];

        ((unsigned char*)(cur_line))[0] = (clr).r;
        ((unsigned char*)(cur_line))[1] = (clr).g;
        ((unsigned char*)(cur_line))[2] = (clr).b;
        }
      }
    }
    else
      return false;
    }

  return true;
}

//===================================================================
//= Function name	: SaveBitmap
//= Description   : Сохранение bmp в файл
//= Return type   : void 
//===================================================================

bool DSimpleBitmap::SaveBitmap(const char *in_pcFileName)
{
  // Open file  
  FILE *pFile = fopen(in_pcFileName, "wb");
  if (!pFile)
    return false;
  
  int data_size = 3 * GetWidth() * GetHeight();
  
  // File header set & write 
  BITMAPFILEHEADER file_header;
  
  file_header.bfType = MAKEWORD('B', 'M');
  file_header.bfReserved1 = 0;
  file_header.bfReserved2 = 0;
  file_header.bfSize      = 0; //?
  file_header.bfOffBits   = 54;
  
  fwrite(&file_header, sizeof(BITMAPFILEHEADER), 1, pFile);
  
  // Info header set & write
  BITMAPINFOHEADER info_header;
  info_header.biSize          = sizeof(BITMAPINFOHEADER);
  info_header.biWidth         = GetWidth();
  info_header.biHeight        = GetHeight();
  info_header.biPlanes        = 1;
  info_header.biBitCount      = 24;
  info_header.biCompression   = BI_RGB;
  info_header.biSizeImage     = 0;
  info_header.biXPelsPerMeter = 0;
  info_header.biYPelsPerMeter = 0;
  info_header.biClrUsed       = 0;
  info_header.biClrImportant  = 0;
  
  fwrite(&info_header, 1, sizeof(BITMAPINFOHEADER), pFile);
 
  // width should be 'kratna 4m' :)
  int iFullWdt = GetWidth() * 3;
  int correct_width = (iFullWdt) % 4 != 0 ? (iFullWdt / 4 * 4 + 4) : iFullWdt;
  BYTE *data = new BYTE[ correct_width * GetHeight()];
    
  unsigned int id = 0;

  for (int y = 0; y < GetHeight(); y ++)
  {
    memcpy(&data[id], GetLinePointer(GetHeight() - y - 1), 3 * GetWidth());
    id += correct_width;
  }
  
  fwrite(data, 1, GetHeight() * correct_width, pFile);
  
  fflush(pFile);
  fclose(pFile);
  
  delete[] data;

  return true;
}


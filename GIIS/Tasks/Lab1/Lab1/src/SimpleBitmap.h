#if C_GRAPHICSMEDIA_LAB_DMOROZ_C
#/*******************************************************************************
# * (C) Copyright 2003/2004 by Vladimir Vezhnevets <vvp@graphics.cs.msu.su>     *
# *******************************************************************************/
#endif

/** @file  SimpleBitmap.h
 *  @brief ������� ����� ��� ��������, ����������, ��������� � ������� ���������� �����������
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
/// ���������� ����� ��� ������ � ��������� ������������ 

class DSimpleBitmap  
{
  // Attributes
//protected:
public:

  /// ��������� ������ �����������
  BYTE*             m_pBits;            ///< ��������� �� ������ �����������
  HDC               m_hDC;              ///< ���������� device context
  BITMAPINFO        m_BMInfo;           ///< ��������� Bitmap info
  HBITMAP           m_hBMP;             ///< BITMAP handle
  HGDIOBJ           m_hOldHandle;       ///< ��� ���������� ������� ������ ��� ������
  int               m_iBytesPerLine;    ///< ���������� ���� � ������ ����������� 
                                        ///< (����� �� ��������� � '������' * 3!)
  bool              m_bCreated;
// Operations
public:

  /// �������� ����������� �������� ��������
  bool CreateImage(int in_iWidth,  int in_iHeight);

  /// ��������� ������ �����������
  int GetWidth() const;

  /// ��������� ������ �����������
  int GetHeight() const;

  /// ��������� ��������� �� ������ ������
  /// @returns ��������� �� ������ ������ 'in_iLineNumber', ���� ������ ����������
  unsigned char *GetLinePointer(int in_iLineNumber);

  /// �������� bmp �� �����
  bool LoadBitmap(const char *in_pcFileName);

  /// ���������� bmp � ����
  bool SaveBitmap(const char *in_pcFileName);

  /// ������� ��������� � DC
  void Paint(HDC in_DC);

  /// �������� ������������
  DSimpleBitmap &operator = (const DSimpleBitmap &in_Image);

protected:
  /// ��������� ���������� ������ ������
  void ResetValues();
  /// ������� ������
  void FreeMembers();

  /// ��������������� ������� ��� ������ bmp
  bool ReadFileHeader(FILE *in_pFile, int &bitmap_pos);

public:
	DSimpleBitmap();
	DSimpleBitmap(const DSimpleBitmap &in_Image);

	virtual ~DSimpleBitmap();
};

#endif // !defined(AFX_SIMPLEBITMAP_H__7957C2E8_D502_401C_A87F_2F2A9EE7A46F__INCLUDED_)

void WhiteNoise(DSimpleBitmap *img, int Noise)
{
	if(Noise==0)
		return;
	int wdth=(img->GetWidth()*3+3)&-4;
	unsigned char *B=(unsigned char *)img->GetLinePointer(0);
  for(int y=0; y<img->GetHeight(); y++) for (int x=0; x<img->GetWidth(); x++)
  {
    B[y*wdth+x*3+0]=crop(B[y*wdth+x*3+0]+random(Noise)-random(Noise),0,255);
    B[y*wdth+x*3+1]=crop(B[y*wdth+x*3+1]+random(Noise)-random(Noise),0,255);
    B[y*wdth+x*3+2]=crop(B[y*wdth+x*3+2]+random(Noise)-random(Noise),0,255);
  }
}
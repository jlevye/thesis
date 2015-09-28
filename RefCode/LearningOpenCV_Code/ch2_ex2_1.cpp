/* License:
   Oct. 3, 2008
   Right to use this code in any way you want without warrenty, support or any guarentee of it working.

   BOOK: It would be nice if you cited it:
   Learning OpenCV: Computer Vision with the OpenCV Library
     by Gary Bradski and Adrian Kaehler
     Published by O'Reilly Media, October 3, 2008

   AVAILABLE AT:
     http://www.amazon.com/Learning-OpenCV-Computer-Vision-Library/dp/0596516134
     Or: http://oreilly.com/catalog/9780596516130/
     ISBN-10: 0596516134 or: ISBN-13: 978-0596516130

   OTHER OPENCV SITES:
   * The source code is on sourceforge at:
     http://sourceforge.net/projects/opencvlibrary/
   * The OpenCV wiki page (As of Oct 1, 2008 this is down for changing over servers, but should come back):
     http://opencvlibrary.sourceforge.net/
   * An active user group is at:
     http://tech.groups.yahoo.com/group/OpenCV/
   * The minutes of weekly OpenCV development meetings are at:
     http://pr.willowgarage.com/wiki/OpenCV
*/
#include "highgui.h"

int main( int argc, char** argv )
{
  //Designates variable - this is the main opencv image type and loads the image specified in the main call
  IplImage* img = cvLoadImage( argv[1] );
  //Makes a window to look at it in
  cvNamedWindow("Example1", CV_WINDOW_AUTOSIZE );
  //Shows the image
  cvShowImage("Example1", img );
  cvWaitKey(0);
  //Gets rid of image (frees memory) and closes window on keypress
  cvReleaseImage( &img );
  cvDestroyWindow("Example1");
}

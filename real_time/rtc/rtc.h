#ifndef _RTC_H
#define _RTC_H

/**
* Initialize the RTC clock with the given speed, and enable interruptions
*
* Take into account that, as RTC could be really quick compared to your code, you may need to
* clean the file descriptor the first time, calling the rtc_tick() function
*
* @param speed Integer from 2 up to 8192, as power of 2, which represents the interruption
*     frecuency in Hertz
* @returns rtc_fd The file descriptor to the RTC with the interruptions already enabled
* @see [rtc driver](https://android.googlesource.com/kernel/omap/+/glass-omap-xrr02/Documentation/rtc.txt)
* @see [file descriptors](https://en.wikipedia.org/wiki/File_descriptor)
*/
int rtc_init(int speed);

/**
* Wait until an RTC interruption occurs, or clean the file descriptor if one has already passed
*
* @see [rtc driver](https://android.googlesource.com/kernel/omap/+/glass-omap-xrr02/Documentation/rtc.txt)
*/
void rtc_tick(void);

/**
* Disable interruptions and close RTC file descriptor.
*
* Should be called when the RTC interruptions are not needed no more, to properly stop them
* @see [rtc driver](https://android.googlesource.com/kernel/omap/+/glass-omap-xrr02/Documentation/rtc.txt)
* @see [file descriptors](https://en.wikipedia.org/wiki/File_descriptor)
*/
void rtc_close(void);

#endif
#ifndef _RTC_H
#define _RTC_H

int rtc_init(int speed);
void rtc_tick(void);
void rtc_close(void);

#endif
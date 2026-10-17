package main

import (
	"errors"
	"time"
)

// DaysUntilDeadline calculates the number of days between currentDate and deadline.
// Dates must be in "YYYY-MM-DD" format. Returns an error if dates are invalid or deadline is before currentDate.
func DaysUntilDeadline(currentDate, deadline string) (int, error) {
	layout := "2006-01-02"
	current, err := time.Parse(layout, currentDate)
	if err != nil {
		return 0, errors.New("invalid current date format")
	}
	due, err := time.Parse(layout, deadline)
	if err != nil {
		return 0, errors.New("invalid deadline format")
	}
	if due.Before(current) {
		return 0, errors.New("deadline cannot be before current date")
	}
	// Count from Unix seconds rather than due.Sub(current): a time.Duration
	// (int64 nanoseconds) saturates at about 292 years.
	// 86400 = 60 seconds x 60 minutes x 24 hours = number of seconds in a day.
	days := int((due.Unix() - current.Unix()) / 86400)
	return days, nil
}

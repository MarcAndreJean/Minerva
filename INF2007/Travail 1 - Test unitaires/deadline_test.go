package main

import (
	"errors"
	"testing"
	"time"
)

// Errors expected from DaysUntilDeadline, compared by message.
var (
	errCurrent  = errors.New("invalid current date format")
	errDeadline = errors.New("invalid deadline format")
	errBefore   = errors.New("deadline cannot be before current date")
)

// Verifies that valid dates, with a deadline on the same day or later,
// return the correct number of days and no error.
func TestDaysUntilDeadlineValid(t *testing.T) {
	tests := []struct {
		name        string
		currentDate string
		deadline    string
		expected    int
	}{
		{"future deadline", "2025-05-26", "2025-06-01", 6},
		{"same day", "2025-05-26", "2025-05-26", 0},
		{"largest gap", "0000-01-01", "9999-12-31", 3652424},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			days, err := DaysUntilDeadline(tt.currentDate, tt.deadline)
			if err != nil {
				t.Errorf("DaysUntilDeadline(%q, %q): unexpected error %v", tt.currentDate, tt.deadline, err)
			}
			if days != tt.expected {
				t.Errorf("DaysUntilDeadline(%q, %q) = %d; expected %d", tt.currentDate, tt.deadline, days, tt.expected)
			}
		})
	}
}

// Verifies that a deadline date prior to the current date is rejected.
func TestDaysUntilDeadlineBeforeCurrent(t *testing.T) {
	days, err := DaysUntilDeadline("2025-05-26", "1999-05-26")
	if err == nil {
		t.Fatalf("expected error %q, got none", errBefore)
	}
	if err.Error() != errBefore.Error() {
		t.Errorf("error %q; expected %q", err, errBefore)
	}
	if days != 0 {
		t.Errorf("days = %d; expected 0 on error", days)
	}
}

// Verifies that a date in the right format but that does not exist,
// in either parameter, returns 0 and the matching error message.
func TestDaysUntilDeadlineInvalidDate(t *testing.T) {
	tests := []struct {
		name        string
		currentDate string
		deadline    string
		expectedErr error
	}{
		{"invalid current date", "2025-13-01", "2025-06-01", errCurrent},
		{"current date with day 31 in a 30-day month", "2025-04-31", "2025-06-01", errCurrent},
		{"invalid deadline", "2025-05-26", "2025-13-01", errDeadline},
		{"deadline with day 31 in a 30-day month", "2025-05-26", "2025-06-31", errDeadline},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			days, err := DaysUntilDeadline(tt.currentDate, tt.deadline)
			if err == nil {
				t.Fatalf("DaysUntilDeadline(%q, %q): expected error %q, got none", tt.currentDate, tt.deadline, tt.expectedErr)
			}
			if err.Error() != tt.expectedErr.Error() {
				t.Errorf("DaysUntilDeadline(%q, %q): error %q; expected %q", tt.currentDate, tt.deadline, err, tt.expectedErr)
			}
			if days != 0 {
				t.Errorf("DaysUntilDeadline(%q, %q) = %d; expected 0 on error", tt.currentDate, tt.deadline, days)
			}
		})
	}
}

// Verifies that a date that does not follow the "YYYY-MM-DD" format,
// in either parameter, returns 0 and the matching error message.
func TestDaysUntilDeadlineMalformedDate(t *testing.T) {
	tests := []struct {
		name        string
		currentDate string
		deadline    string
		expectedErr error
	}{
		{"malformed current date", "2025/05/26", "2025-06-01", errCurrent},
		{"empty current date", "", "2025-06-01", errCurrent},
		{"malformed deadline", "2025-05-26", "2025/05/26", errDeadline},
		{"empty deadline", "2025-05-26", "", errDeadline},
		// Both dates invalid: the function checks currentDate first, so it returns errCurrent.
		{"both invalid", "2025/05/26", "2025-13-01", errCurrent},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			days, err := DaysUntilDeadline(tt.currentDate, tt.deadline)
			if err == nil {
				t.Fatalf("DaysUntilDeadline(%q, %q): expected error %q, got none", tt.currentDate, tt.deadline, tt.expectedErr)
			}
			if err.Error() != tt.expectedErr.Error() {
				t.Errorf("DaysUntilDeadline(%q, %q): error %q; expected %q", tt.currentDate, tt.deadline, err, tt.expectedErr)
			}
			if days != 0 {
				t.Errorf("DaysUntilDeadline(%q, %q) = %d; expected 0 on error", tt.currentDate, tt.deadline, days)
			}
		})
	}
}

// Verifies, with generated strings, that DaysUntilDeadline never panics,
// returns 0 on error, and that adding the returned days to currentDate
// gives the deadline.
func FuzzDaysUntilDeadline(f *testing.F) {
	f.Add("2025-05-26", "2025-06-01")
	f.Add("2025-05-26", "2025/05/26")
	f.Add("", "")

	f.Fuzz(func(t *testing.T, currentDate, deadline string) {
		days, err := DaysUntilDeadline(currentDate, deadline)
		if err != nil {
			if days != 0 {
				t.Errorf("DaysUntilDeadline(%q, %q) = %d; expected 0 on error", currentDate, deadline, days)
			}
			return
		}

		// No error means currentDate is a valid date.
		start, _ := time.Parse("2006-01-02", currentDate)
		if got := start.AddDate(0, 0, days).Format("2006-01-02"); got != deadline {
			t.Errorf("DaysUntilDeadline(%q, %q) = %d, but %s + %d days = %s", currentDate, deadline, days, currentDate, days, got)
		}
	})
}

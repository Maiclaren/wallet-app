-- GUI -- 

Application: Superclass με constructor τη ρίζα (root) του γραφικού περιβάλλοντος της εφαρμογής και μια method για το ποιο από τα παρακάτω Frame θα ανοίγει κατά περίπτωση:
Frames (subclasses of Application)
1.	Welcome frame: Subclass της Application με δυνατότητα επιλογής sign up or in στην εφαρμογή.
2.	Sign up frame: Καταχώρηση username & password και αποθήκευση σε sql lite table
3.	Sign in frame: Validation συμπληρωμένων πεδίων από sql lite table.  
4.	Main frame: Αποτελεί το main frame της εφαρμογής με κάποια σύντομα στατιστικά του account σε ήδη εγγεγραμμένο χρήστη καθώς και επιλογή δημιουργία νέων Εσόδων / Εξόδων / Οφειλών / Επιθυμιών ή αναλυτική επισκόπηση υπαρχόντων. (Πιθανή εισαγωγή matplotlib bar ή line chart)
5.	Input Frame: Frame δημιουργίας νέων Εσόδων / Εξόδων / Οφειλών / Επιθυμιών.
6.	Inspect Frame: Frame επισκόπησης υπαρχόντων Εσόδων / Εξόδων / Οφειλών / Επιθυμιών με export σε excel button. 

--SQL Lite--

Καταχώρηση και αναζήτηση από αυτήν όλων των εγγραφών που αφορούν Έσοδο / Έξοδο / Οφειλή / Επιθυμίας. 
Ένας πίνακας για όλους τους τύπους εγγραφής με απλό primary key (ΑΑ: ο οποίος θα δημιουργείται αυτόματα)  για πιο εύκολη αναζήτηση εγγραφής από χρήστη και πιο απλή αρχιτεκτονική. Το κατηγόρημα του πίνακα ‘Τύπος εγγραφής’ θα ορίζει συνώνυμα και τον τύπο εγγραφής.
Ένας πίνακας για καταχώρηση χρηστών (username – password) & primary key το username προς αποφυγή δημιουργίας accounts με το ίδιο.

--ΕΓΓΡΑΦΕΣ--

Δύο Υπερκλάσεις: 
1.	Exchange
Με αντιστοίχως δύο υποκλάσεις: 
a.	Revenue (Έσοδο): name, amount, date
b.	Expense (Έξοδο): name, amount, date

2.	Task
Ομοίως με δύο Υποκλάσεις:
a.	Obligation: name, amount, date, status
b.	Wishlist: name, amount, date, status, link




--
-- Database: `pathshala`
-- for SQLite only
--copy and paste it in sqlite terminal

-- --------------------------------------------------------

--
-- Table structure for table `comments`
--
CREATE TABLE IF NOT EXISTS `contacts` (
  `sno` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `name` text NOT NULL,
  `phone_num` text NOT NULL,
  `msg` text NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `email` text NOT NULL
);


CREATE TABLE IF NOT EXISTS `comments` (
  `sno` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `id` integer NOT NULL,
  `user` text NOT NULL DEFAULT 'admin',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `comment` text NOT NULL
);

--
-- Dumping data for table `comments`
--

INSERT INTO `comments` (`sno`, `id`, `user`, `timestamp`, `comment`) VALUES
(1, 1, 'Vishal', '2019-03-16 12:40:40', 'Test Comment'),
(2, 2, 'Raj', '2019-03-16 12:40:40', 'Another Test Comment'),
(3, 1, 'admin', '2019-03-16 13:19:43', 'another test comment'),
(4, 2, 'admin', '2019-03-16 13:20:15', 'its working'),
(5, 0, 'admin', '2019-03-16 15:01:02', 'comment count test'),
(6, 0, 'admin', '2019-03-16 15:01:17', 'adfasd'),
(7, 1, 'admin', '2019-03-16 15:02:29', 'test comment to count');

-- --------------------------------------------------------

--
-- Table structure for table `playlist`
--

CREATE TABLE IF NOT EXISTS `playlist` (
  `sno` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `Title` text NOT NULL,
  `slug` text NOT NULL,
  `tagline` text NOT NULL
);

--
-- Dumping data for table `playlist`
--

INSERT INTO `playlist` (`sno`, `Title`, `slug`, `tagline`) VALUES
(1, 'Python Tutorials For Absolute Beginners In Hindi', 'python-tutorials-for-absolute-beginners', 'In this series, we will learn about Python Tutorials For Beginners In Hindi. Click Start Watching button below to start watching this series of videos.'),
(2, 'Artificial intelligence Series in HINDI', 'Artificial-intelligence-Series-in-HINDI', 'In this series, we will learn about Artificial intelligence Series in HINDI. Click Start Watching button below to start watching this series of videos.'),
(3, 'Machine Learning', 'Machine-Learning', 'In this tutorial we will learn about machine learning.Click Start Watching button below to start watching this series of videos.'),
(4, 'Information and cyber security', 'Information-and-cyber-security', 'In this tutorial we will learn about Information and cyber security.Click Start Watching button below to start watching this series of videos.');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE IF NOT EXISTS `user` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `username` text NOT NULL,
  `password` text NOT NULL,
  `email` text NOT NULL,
  `image_file` text NOT NULL DEFAULT 'default.jpg'
);

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `password`, `email`, `image_file`) VALUES
(1, 'vishal', '$2b$12$mGLu32A2hp0S7mlDkdbi3OjDCG3EEojXOiY.N6VDyrX47qboy5uuy', 'vishal@mail.com', 'default.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `videos`
--

CREATE TABLE IF NOT EXISTS `videos` (
  `ID` integer NOT NULL PRIMARY KEY AUTOINCREMENT ,
  `sno` integer NOT NULL,
  `title` text NOT NULL,
  `link` text NOT NULL
);

--
-- Dumping data for table `videos`
--

INSERT INTO `videos` (`ID`, `sno`, `title`, `link`) VALUES
(1, 1, 'Introduction to Python in Hindi | Part 1 | Python Tutorial For Beginners Series #1', 'gx02MBUtTdM'),
(2, 1, 'Basics of Python in hindi | part 2 | Python Tutorial for Beginners #2', 'hQzbePDFO9I'),
(3, 3, 'Introduction To Machine Learning ll Machine Learning Course Explained With RealLife Examples (Hindi)', 'Y4qO9unerGs'),
(4, 3, 'Classic Machine and Adaptive Machine || Machine Learning Course', 'YHcAQKrh3E4'),
(5, 4, 'Elements Of Information Security ll Information and Cyber Security Course Explained in Hindi', 'lvARQKJnwp0'),
(6, 4, 'Security Policy ll Information And Cyber Security Course Explained in Hindi', 'cMOWZkYVleg');

--
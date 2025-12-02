-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Nov 17, 2025 at 02:16 PM
-- Server version: 10.11.14-MariaDB-cll-lve
-- PHP Version: 8.4.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `uaackwis_farm_agrobot`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add Weekly Attendance Summary', 7, 'add_attendanceweeklysummary'),
(26, 'Can change Weekly Attendance Summary', 7, 'change_attendanceweeklysummary'),
(27, 'Can delete Weekly Attendance Summary', 7, 'delete_attendanceweeklysummary'),
(28, 'Can view Weekly Attendance Summary', 7, 'view_attendanceweeklysummary'),
(29, 'Can add Crop', 8, 'add_crop'),
(30, 'Can change Crop', 8, 'change_crop'),
(31, 'Can delete Crop', 8, 'delete_crop'),
(32, 'Can view Crop', 8, 'view_crop'),
(33, 'Can add crop variant', 9, 'add_cropvariant'),
(34, 'Can change crop variant', 9, 'change_cropvariant'),
(35, 'Can delete crop variant', 9, 'delete_cropvariant'),
(36, 'Can view crop variant', 9, 'view_cropvariant'),
(37, 'Can add employee', 10, 'add_employee'),
(38, 'Can change employee', 10, 'change_employee'),
(39, 'Can delete employee', 10, 'delete_employee'),
(40, 'Can view employee', 10, 'view_employee'),
(41, 'Can add expense', 11, 'add_expense'),
(42, 'Can change expense', 11, 'change_expense'),
(43, 'Can delete expense', 11, 'delete_expense'),
(44, 'Can view expense', 11, 'view_expense'),
(45, 'Can add Farm Segment', 12, 'add_farmsegment'),
(46, 'Can change Farm Segment', 12, 'change_farmsegment'),
(47, 'Can delete Farm Segment', 12, 'delete_farmsegment'),
(48, 'Can view Farm Segment', 12, 'view_farmsegment'),
(49, 'Can add Job', 13, 'add_job'),
(50, 'Can change Job', 13, 'change_job'),
(51, 'Can delete Job', 13, 'delete_job'),
(52, 'Can view Job', 13, 'view_job'),
(53, 'Can add merchant', 14, 'add_merchant'),
(54, 'Can change merchant', 14, 'change_merchant'),
(55, 'Can delete merchant', 14, 'delete_merchant'),
(56, 'Can view merchant', 14, 'view_merchant'),
(57, 'Can add Sale', 15, 'add_sale'),
(58, 'Can change Sale', 15, 'change_sale'),
(59, 'Can delete Sale', 15, 'delete_sale'),
(60, 'Can view Sale', 15, 'view_sale'),
(61, 'Can add Yield', 16, 'add_yield'),
(62, 'Can change Yield', 16, 'change_yield'),
(63, 'Can delete Yield', 16, 'delete_yield'),
(64, 'Can view Yield', 16, 'view_yield'),
(65, 'Can add Weekly Wage Payment', 17, 'add_weeklywagepayment'),
(66, 'Can change Weekly Wage Payment', 17, 'change_weeklywagepayment'),
(67, 'Can delete Weekly Wage Payment', 17, 'delete_weeklywagepayment'),
(68, 'Can view Weekly Wage Payment', 17, 'view_weeklywagepayment'),
(69, 'Can add Wage Payment Transaction', 18, 'add_wagepaymenttransaction'),
(70, 'Can change Wage Payment Transaction', 18, 'change_wagepaymenttransaction'),
(71, 'Can delete Wage Payment Transaction', 18, 'delete_wagepaymenttransaction'),
(72, 'Can view Wage Payment Transaction', 18, 'view_wagepaymenttransaction'),
(73, 'Can add Wage', 19, 'add_wage'),
(74, 'Can change Wage', 19, 'change_wage'),
(75, 'Can delete Wage', 19, 'delete_wage'),
(76, 'Can view Wage', 19, 'view_wage'),
(77, 'Can add sale variant', 20, 'add_salevariant'),
(78, 'Can change sale variant', 20, 'change_salevariant'),
(79, 'Can delete sale variant', 20, 'delete_salevariant'),
(80, 'Can view sale variant', 20, 'view_salevariant'),
(81, 'Can add job farm segment', 21, 'add_jobfarmsegment'),
(82, 'Can change job farm segment', 21, 'change_jobfarmsegment'),
(83, 'Can delete job farm segment', 21, 'delete_jobfarmsegment'),
(84, 'Can view job farm segment', 21, 'view_jobfarmsegment'),
(85, 'Can add job employee', 22, 'add_jobemployee'),
(86, 'Can change job employee', 22, 'change_jobemployee'),
(87, 'Can delete job employee', 22, 'delete_jobemployee'),
(88, 'Can view job employee', 22, 'view_jobemployee'),
(89, 'Can add Attendance Record', 23, 'add_attendancerecord'),
(90, 'Can change Attendance Record', 23, 'change_attendancerecord'),
(91, 'Can delete Attendance Record', 23, 'delete_attendancerecord'),
(92, 'Can view Attendance Record', 23, 'view_attendancerecord'),
(93, 'Can add yield variant', 24, 'add_yieldvariant'),
(94, 'Can change yield variant', 24, 'change_yieldvariant'),
(95, 'Can delete yield variant', 24, 'delete_yieldvariant'),
(96, 'Can view yield variant', 24, 'view_yieldvariant'),
(97, 'Can add yield farm segment', 25, 'add_yieldfarmsegment'),
(98, 'Can change yield farm segment', 25, 'change_yieldfarmsegment'),
(99, 'Can delete yield farm segment', 25, 'delete_yieldfarmsegment'),
(100, 'Can view yield farm segment', 25, 'view_yieldfarmsegment'),
(101, 'Can add bulk wage payment', 26, 'add_bulkwagepayment'),
(102, 'Can change bulk wage payment', 26, 'change_bulkwagepayment'),
(103, 'Can delete bulk wage payment', 26, 'delete_bulkwagepayment'),
(104, 'Can view bulk wage payment', 26, 'view_bulkwagepayment'),
(105, 'Can add bill image', 27, 'add_billimage'),
(106, 'Can change bill image', 27, 'change_billimage'),
(107, 'Can delete bill image', 27, 'delete_billimage'),
(108, 'Can view bill image', 27, 'view_billimage'),
(109, 'Can add payment history', 28, 'add_paymenthistory'),
(110, 'Can change payment history', 28, 'change_paymenthistory'),
(111, 'Can delete payment history', 28, 'delete_paymenthistory'),
(112, 'Can view payment history', 28, 'view_paymenthistory'),
(113, 'Can add sale image', 29, 'add_saleimage'),
(114, 'Can change sale image', 29, 'change_saleimage'),
(115, 'Can delete sale image', 29, 'delete_saleimage'),
(116, 'Can view sale image', 29, 'view_saleimage'),
(117, 'Can add scraped event', 30, 'add_scrapedevent'),
(118, 'Can change scraped event', 30, 'change_scrapedevent'),
(119, 'Can delete scraped event', 30, 'delete_scrapedevent'),
(120, 'Can view scraped event', 30, 'view_scrapedevent');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `bulk_wage_payments`
--

CREATE TABLE `bulk_wage_payments` (
  `id` bigint(20) NOT NULL,
  `week_start_date` date NOT NULL,
  `week_end_date` date NOT NULL,
  `payment_date` datetime(6) NOT NULL,
  `employee_payments` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`employee_payments`)),
  `total_employees` int(11) NOT NULL,
  `total_amount` decimal(15,2) NOT NULL,
  `payment_mode` varchar(20) NOT NULL,
  `payment_reference` varchar(100) NOT NULL,
  `remarks` longtext NOT NULL,
  `expense_category` varchar(50) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `paid_by_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session'),
(23, 'xe_farm', 'attendancerecord'),
(7, 'xe_farm', 'attendanceweeklysummary'),
(27, 'xe_farm', 'billimage'),
(26, 'xe_farm', 'bulkwagepayment'),
(8, 'xe_farm', 'crop'),
(9, 'xe_farm', 'cropvariant'),
(10, 'xe_farm', 'employee'),
(11, 'xe_farm', 'expense'),
(12, 'xe_farm', 'farmsegment'),
(13, 'xe_farm', 'job'),
(22, 'xe_farm', 'jobemployee'),
(21, 'xe_farm', 'jobfarmsegment'),
(14, 'xe_farm', 'merchant'),
(28, 'xe_farm', 'paymenthistory'),
(15, 'xe_farm', 'sale'),
(29, 'xe_farm', 'saleimage'),
(20, 'xe_farm', 'salevariant'),
(30, 'xe_farm', 'scrapedevent'),
(19, 'xe_farm', 'wage'),
(18, 'xe_farm', 'wagepaymenttransaction'),
(17, 'xe_farm', 'weeklywagepayment'),
(16, 'xe_farm', 'yield'),
(25, 'xe_farm', 'yieldfarmsegment'),
(24, 'xe_farm', 'yieldvariant');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-08-09 13:54:34.304511'),
(2, 'auth', '0001_initial', '2025-08-09 13:54:34.341821'),
(3, 'admin', '0001_initial', '2025-08-09 13:54:34.352550'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-08-09 13:54:34.357203'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-08-09 13:54:34.362989'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-08-09 13:54:34.375703'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-08-09 13:54:34.381401'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-08-09 13:54:34.387244'),
(9, 'auth', '0004_alter_user_username_opts', '2025-08-09 13:54:34.391807'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-08-09 13:54:34.398401'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-08-09 13:54:34.398870'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-08-09 13:54:34.403428'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-08-09 13:54:34.409288'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-08-09 13:54:34.416093'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-08-09 13:54:34.421682'),
(16, 'auth', '0011_update_proxy_permissions', '2025-08-09 13:54:34.426476'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-08-09 13:54:34.431792'),
(18, 'sessions', '0001_initial', '2025-08-09 13:54:34.435107'),
(19, 'xe_farm', '0001_initial', '2025-08-09 13:54:34.588714'),
(20, 'xe_farm', '0002_bulkwagepayment', '2025-08-09 13:54:34.604784'),
(21, 'xe_farm', '0003_alter_weeklywagepayment_options_and_more', '2025-08-20 06:19:34.091377'),
(22, 'xe_farm', '0004_remove_weeklywagepayment_unique_employee_weekly_payment_and_more', '2025-08-20 07:31:44.998500'),
(23, 'xe_farm', '0005_remove_weeklywagepayment_unique_employee_weekly_payment_and_more', '2025-08-20 07:33:48.795731'),
(24, 'xe_farm', '0006_remove_weeklywagepayment_unique_employee_weekly_payment_and_more', '2025-08-20 08:16:38.988342'),
(25, 'xe_farm', '0007_remove_weeklywagepayment_unique_employee_weekly_payment_and_more', '2025-08-23 10:18:14.921855'),
(26, 'xe_farm', '0008_remove_weeklywagepayment_unique_employee_weekly_payment_and_more', '2025-08-23 10:18:14.922519'),
(27, 'xe_farm', '0009_remove_weeklywagepayment_unique_employee_weekly_payment_and_more', '2025-08-23 10:18:52.958370'),
(28, 'xe_farm', '0010_remove_weeklywagepayment_unique_employee_weekly_payment_and_more', '2025-10-23 09:30:20.904933'),
(29, 'xe_farm', '0011_remove_weeklywagepayment_unique_employee_weekly_payment_and_more', '2025-10-23 09:30:20.905657'),
(30, 'xe_farm', '0012_remove_weeklywagepayment_unique_employee_weekly_payment_and_more', '2025-10-23 09:30:20.915487'),
(31, 'xe_farm', '0013_remove_weeklywagepayment_unique_employee_weekly_payment_and_more', '2025-10-23 09:30:20.916004'),
(32, 'xe_farm', '0014_remove_weeklywagepayment_unique_employee_weekly_payment_and_more', '2025-10-23 09:30:20.924856'),
(33, 'xe_farm', '0015_billimage_and_more', '2025-10-23 09:30:20.925390'),
(34, 'xe_farm', '0016_billimage_and_more', '2025-10-23 09:30:20.943710'),
(35, 'xe_farm', '0017_paymenthistory_saleimage_and_more', '2025-10-23 09:30:20.944243'),
(36, 'xe_farm', '0018_paymenthistory_saleimage_and_more', '2025-10-23 09:30:21.005206'),
(37, 'xe_farm', '0019_remove_weeklywagepayment_unique_employee_weekly_payment_and_more', '2025-10-23 09:30:21.005743'),
(38, 'xe_farm', '0020_remove_weeklywagepayment_unique_employee_weekly_payment_and_more', '2025-10-23 09:34:03.832007'),
(39, 'xe_farm', '0021_scrapedevent', '2025-11-06 11:13:58.428563');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `farm_segments`
--

CREATE TABLE `farm_segments` (
  `id` bigint(20) NOT NULL,
  `farm_name` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `farm_segments`
--

INSERT INTO `farm_segments` (`id`, `farm_name`, `created_at`, `updated_at`) VALUES
(3, 'veetadi', '2025-11-07 12:19:33.632183', '2025-11-07 12:19:33.632245'),
(4, 'thaani marathu kuttu', '2025-11-07 12:20:15.281230', '2025-11-07 12:20:15.281292'),
(5, 'full xe', '2025-11-07 12:20:26.226350', '2025-11-07 12:20:26.226380'),
(6, 'mudakku thorai', '2025-11-07 12:20:35.225589', '2025-11-07 12:20:35.225618'),
(7, 'vazhukadu', '2025-11-07 12:20:43.222009', '2025-11-07 12:20:43.222034'),
(8, 'keppa kaadu', '2025-11-07 12:20:51.911517', '2025-11-07 12:20:51.911546');

-- --------------------------------------------------------

--
-- Table structure for table `xe_attendance_records`
--

CREATE TABLE `xe_attendance_records` (
  `id` bigint(20) NOT NULL,
  `date` date NOT NULL,
  `attendance_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`attendance_data`)),
  `created_at` datetime(6) NOT NULL,
  `last_updated` datetime(6) NOT NULL,
  `created_by_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `xe_attendance_records`
--

INSERT INTO `xe_attendance_records` (`id`, `date`, `attendance_data`, `created_at`, `last_updated`, `created_by_id`) VALUES
(353, '2025-01-01', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:09.832770', '2025-11-07 12:07:09.832803', NULL),
(354, '2025-02-01', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:09.930802', '2025-11-07 12:07:09.930817', NULL),
(355, '2025-03-01', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:10.028979', '2025-11-07 12:07:10.028999', NULL),
(356, '2025-04-01', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:10.120450', '2025-11-07 12:07:10.120470', NULL),
(357, '2025-05-01', '[{\"employee_id\": \"38\", \"employee_name\": \"Anjali\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"47\", \"employee_name\": \"Dev\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-04-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"50\", \"employee_name\": \"Guru\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"39\", \"employee_name\": \"Julie\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"42\", \"employee_name\": \"Lakshmi\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"46\", \"employee_name\": \"Rajendhiran\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"48\", \"employee_name\": \"Sameer\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:10.289694', '2025-11-07 12:07:10.289713', NULL),
(358, '2025-07-01', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:10.420395', '2025-11-07 12:07:10.420411', NULL),
(359, '2025-08-01', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:10.541139', '2025-11-07 12:07:10.541157', NULL),
(360, '2025-09-01', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:10.640486', '2025-11-07 12:07:10.640502', NULL),
(361, '2025-11-01', '[{\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:10.719578', '2025-11-07 12:07:10.719593', NULL),
(362, '2025-01-02', '[{\"employee_id\": \"40\", \"employee_name\": \"Kumar\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:10.821289', '2025-11-07 12:07:10.821303', NULL),
(363, '2025-04-02', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:10.910123', '2025-11-07 12:07:10.910142', NULL),
(364, '2025-05-02', '[{\"employee_id\": \"38\", \"employee_name\": \"Anjali\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"39\", \"employee_name\": \"Julie\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"42\", \"employee_name\": \"Lakshmi\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"48\", \"employee_name\": \"Sameer\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"47\", \"employee_name\": \"Dev\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-04-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"46\", \"employee_name\": \"Rajendhiran\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:11.067219', '2025-11-07 12:07:11.067238', NULL),
(365, '2025-06-02', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 0, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:11.141757', '2025-11-07 12:07:11.141775', NULL),
(366, '2025-07-02', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:11.264572', '2025-11-07 12:07:11.264591', NULL),
(367, '2025-08-02', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:11.394121', '2025-11-07 12:07:11.394139', NULL),
(368, '2025-09-02', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:11.504961', '2025-11-07 12:07:11.504980', NULL),
(369, '2024-11-02', '[{\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:11.571686', '2025-11-07 12:07:11.571705', NULL),
(370, '2024-12-02', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"40\", \"employee_name\": \"Kumar\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:11.678228', '2025-11-07 12:07:11.678246', NULL),
(371, '2025-01-03', '[{\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"40\", \"employee_name\": \"Kumar\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:11.784729', '2025-11-07 12:07:11.784748', NULL),
(372, '2025-02-03', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 0, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:11.867991', '2025-11-07 12:07:11.868008', NULL),
(373, '2025-03-03', '[{\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:11.959019', '2025-11-07 12:07:11.959037', NULL),
(374, '2025-04-03', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:12.082452', '2025-11-07 12:07:12.082469', NULL),
(375, '2025-05-03', '[{\"employee_id\": \"38\", \"employee_name\": \"Anjali\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"47\", \"employee_name\": \"Dev\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-04-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"39\", \"employee_name\": \"Julie\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"42\", \"employee_name\": \"Lakshmi\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"46\", \"employee_name\": \"Rajendhiran\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"48\", \"employee_name\": \"Sameer\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:12.252172', '2025-11-07 12:07:12.252191', NULL),
(376, '2025-06-03', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"49\", \"employee_name\": \"Soma Topno\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:12.360401', '2025-11-07 12:07:12.360418', NULL),
(377, '2025-07-03', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:12.481818', '2025-11-07 12:07:12.481837', NULL),
(378, '2025-09-03', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:12.595498', '2025-11-07 12:07:12.595517', NULL),
(379, '2025-11-03', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:12.701966', '2025-11-07 12:07:12.701984', NULL),
(380, '2024-12-03', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"40\", \"employee_name\": \"Kumar\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:12.816944', '2025-11-07 12:07:12.816962', NULL),
(381, '2025-01-04', '[{\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"40\", \"employee_name\": \"Kumar\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:12.930832', '2025-11-07 12:07:12.930858', NULL),
(382, '2025-02-04', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:13.032533', '2025-11-07 12:07:13.032551', NULL),
(383, '2025-03-04', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:13.105146', '2025-11-07 12:07:13.105162', NULL),
(384, '2025-04-04', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:13.180835', '2025-11-07 12:07:13.180853', NULL),
(385, '2025-06-04', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"49\", \"employee_name\": \"Soma Topno\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:13.303372', '2025-11-07 12:07:13.303390', NULL),
(386, '2025-07-04', '[{\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:13.432844', '2025-11-07 12:07:13.432863', NULL),
(387, '2025-08-04', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:13.528941', '2025-11-07 12:07:13.528959', NULL),
(388, '2024-11-04', '[{\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"40\", \"employee_name\": \"Kumar\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 0, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:13.634154', '2025-11-07 12:07:13.634172', NULL),
(389, '2025-11-04', '[{\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:13.746723', '2025-11-07 12:07:13.746741', NULL),
(390, '2024-12-04', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:13.812483', '2025-11-07 12:07:13.812500', NULL),
(391, '2025-01-05', '[{\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:13.935737', '2025-11-07 12:07:13.935766', NULL),
(392, '2025-02-05', '[{\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:14.056043', '2025-11-07 12:07:14.056062', NULL),
(393, '2025-03-05', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:14.129882', '2025-11-07 12:07:14.129901', NULL),
(394, '2025-04-05', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:14.207403', '2025-11-07 12:07:14.207421', NULL),
(395, '2025-05-05', '[{\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:14.313087', '2025-11-07 12:07:14.313102', NULL),
(396, '2025-06-05', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"49\", \"employee_name\": \"Soma Topno\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:14.423705', '2025-11-07 12:07:14.423725', NULL);
INSERT INTO `xe_attendance_records` (`id`, `date`, `attendance_data`, `created_at`, `last_updated`, `created_by_id`) VALUES
(397, '2025-07-05', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:14.543149', '2025-11-07 12:07:14.543165', NULL),
(398, '2025-08-05', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:14.656940', '2025-11-07 12:07:14.656958', NULL),
(399, '2025-09-05', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:14.768560', '2025-11-07 12:07:14.768577', NULL),
(400, '2024-11-05', '[{\"employee_id\": \"40\", \"employee_name\": \"Kumar\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:14.901518', '2025-11-07 12:07:14.901535', NULL),
(401, '2025-11-05', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:14.989299', '2025-11-07 12:07:14.989317', NULL),
(402, '2024-12-05', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:15.059428', '2025-11-07 12:07:15.059447', NULL),
(403, '2025-01-06', '[{\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"40\", \"employee_name\": \"Kumar\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:15.177393', '2025-11-07 12:07:15.177411', NULL),
(404, '2025-02-06', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:15.281250', '2025-11-07 12:07:15.281268', NULL),
(405, '2025-03-06', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:15.352546', '2025-11-07 12:07:15.352561', NULL),
(406, '2025-05-06', '[{\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:15.478545', '2025-11-07 12:07:15.478563', NULL),
(407, '2025-06-06', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"49\", \"employee_name\": \"Soma Topno\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:15.601010', '2025-11-07 12:07:15.601026', NULL),
(408, '2025-08-06', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:15.708819', '2025-11-07 12:07:15.708838', NULL),
(409, '2025-09-06', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:15.828558', '2025-11-07 12:07:15.828576', NULL),
(410, '2024-11-06', '[{\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"35\", \"employee_name\": \"Marimuthu\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"40\", \"employee_name\": \"Kumar\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:15.940346', '2025-11-07 12:07:15.940363', NULL),
(411, '2025-11-06', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:16.047727', '2025-11-07 12:07:16.047746', NULL),
(412, '2024-12-06', '[{\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"40\", \"employee_name\": \"Kumar\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:16.153921', '2025-11-07 12:07:16.153938', NULL),
(413, '2025-01-07', '[{\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"40\", \"employee_name\": \"Kumar\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:16.264882', '2025-11-07 12:07:16.264901', NULL),
(414, '2025-02-07', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:16.365141', '2025-11-07 12:07:16.365160', NULL),
(415, '2025-03-07', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:16.460644', '2025-11-07 12:07:16.460660', NULL),
(416, '2025-04-07', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"47\", \"employee_name\": \"Dev\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-04-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"48\", \"employee_name\": \"Sameer\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"39\", \"employee_name\": \"Julie\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:16.590087', '2025-11-07 12:07:16.590105', NULL),
(417, '2025-05-07', '[{\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:16.709512', '2025-11-07 12:07:16.709528', NULL),
(418, '2025-06-07', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"49\", \"employee_name\": \"Soma Topno\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:16.824052', '2025-11-07 12:07:16.824068', NULL),
(419, '2025-08-07', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:16.938634', '2025-11-07 12:07:16.938651', NULL),
(420, '2024-11-07', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"35\", \"employee_name\": \"Marimuthu\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"55\", \"employee_name\": \"Nagarajan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:17.073352', '2025-11-07 12:07:17.073369', NULL),
(421, '2025-11-07', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:17.196324', '2025-11-07 12:07:17.196343', NULL),
(422, '2024-12-07', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"40\", \"employee_name\": \"Kumar\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:17.297754', '2025-11-07 12:07:17.297772', NULL),
(423, '2025-01-08', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:17.394216', '2025-11-07 12:07:17.394233', NULL),
(424, '2025-02-08', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:17.505853', '2025-11-07 12:07:17.505871', NULL),
(425, '2025-03-08', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:17.601138', '2025-11-07 12:07:17.601153', NULL),
(426, '2025-04-08', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"47\", \"employee_name\": \"Dev\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-04-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"50\", \"employee_name\": \"Guru\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"39\", \"employee_name\": \"Julie\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"48\", \"employee_name\": \"Sameer\", \"status\": 0, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 0, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:17.744964', '2025-11-07 12:07:17.744983', NULL),
(427, '2025-05-08', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 0, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:17.868000', '2025-11-07 12:07:17.868016', NULL),
(428, '2025-08-08', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:17.975417', '2025-11-07 12:07:17.975434', NULL),
(429, '2025-09-08', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:18.086074', '2025-11-07 12:07:18.086092', NULL),
(430, '2024-11-08', '[{\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"40\", \"employee_name\": \"Kumar\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:18.203133', '2025-11-07 12:07:18.203151', NULL),
(431, '2025-01-09', '[{\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"40\", \"employee_name\": \"Kumar\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:18.339564', '2025-11-07 12:07:18.339584', NULL),
(432, '2025-02-09', '[{\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:18.419689', '2025-11-07 12:07:18.419708', NULL),
(433, '2025-04-09', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 0, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"47\", \"employee_name\": \"Dev\", \"status\": 0, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-04-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"50\", \"employee_name\": \"Guru\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:18.541393', '2025-11-07 12:07:18.541411', NULL),
(434, '2025-05-09', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:18.666057', '2025-11-07 12:07:18.666075', NULL),
(435, '2025-06-09', '[{\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"49\", \"employee_name\": \"Soma Topno\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:18.782671', '2025-11-07 12:07:18.782690', NULL);
INSERT INTO `xe_attendance_records` (`id`, `date`, `attendance_data`, `created_at`, `last_updated`, `created_by_id`) VALUES
(436, '2025-07-09', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"49\", \"employee_name\": \"Soma Topno\", \"status\": 0, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:18.885775', '2025-11-07 12:07:18.885793', NULL),
(437, '2025-08-09', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:18.996309', '2025-11-07 12:07:18.996328', NULL),
(438, '2025-09-09', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:19.114934', '2025-11-07 12:07:19.114952', NULL),
(439, '2024-11-09', '[{\"employee_id\": \"40\", \"employee_name\": \"Kumar\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:19.236719', '2025-11-07 12:07:19.236736', NULL),
(440, '2024-12-09', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:19.333582', '2025-11-07 12:07:19.333602', NULL),
(441, '2025-01-10', '[{\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"40\", \"employee_name\": \"Kumar\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:19.460493', '2025-11-07 12:07:19.460511', NULL),
(442, '2025-03-10', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:19.561392', '2025-11-07 12:07:19.561411', NULL),
(443, '2025-04-10', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 0, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:19.655933', '2025-11-07 12:07:19.655952', NULL),
(444, '2025-07-10', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:19.748425', '2025-11-07 12:07:19.748444', NULL),
(445, '2025-09-10', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:19.854118', '2025-11-07 12:07:19.854135', NULL),
(446, '2025-10-10', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:19.960687', '2025-11-07 12:07:19.960710', NULL),
(447, '2024-12-10', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:20.057608', '2025-11-07 12:07:20.057631', NULL),
(448, '2025-01-11', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"40\", \"employee_name\": \"Kumar\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:20.170304', '2025-11-07 12:07:20.170323', NULL),
(449, '2025-03-11', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:20.266274', '2025-11-07 12:07:20.266291', NULL),
(450, '2025-04-11', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:20.362435', '2025-11-07 12:07:20.362455', NULL),
(451, '2025-06-11', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"49\", \"employee_name\": \"Soma Topno\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 0, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:20.475020', '2025-11-07 12:07:20.475036', NULL),
(452, '2025-07-11', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:20.599324', '2025-11-07 12:07:20.599343', NULL),
(453, '2025-09-11', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:20.752685', '2025-11-07 12:07:20.752704', NULL),
(454, '2025-10-11', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:20.876517', '2025-11-07 12:07:20.876535', NULL),
(455, '2024-11-11', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"40\", \"employee_name\": \"Kumar\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:20.980871', '2025-11-07 12:07:20.980890', NULL),
(456, '2024-12-11', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:21.079746', '2025-11-07 12:07:21.079764', NULL),
(457, '2025-01-12', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 0, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:21.160976', '2025-11-07 12:07:21.160994', NULL),
(458, '2025-03-12', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:21.270099', '2025-11-07 12:07:21.270118', NULL),
(459, '2025-04-12', '[{\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:21.705348', '2025-11-07 12:07:21.705366', NULL),
(460, '2025-07-12', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:21.819788', '2025-11-07 12:07:21.819807', NULL),
(461, '2025-08-12', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:21.912933', '2025-11-07 12:07:21.912950', NULL),
(462, '2025-09-12', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:22.049414', '2025-11-07 12:07:22.049431', NULL),
(463, '2024-11-12', '[{\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"35\", \"employee_name\": \"Marimuthu\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"40\", \"employee_name\": \"Kumar\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:22.153786', '2025-11-07 12:07:22.153804', NULL),
(464, '2025-01-13', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 0, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 0, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"40\", \"employee_name\": \"Kumar\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:22.262115', '2025-11-07 12:07:22.262134', NULL),
(465, '2025-02-13', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:22.357276', '2025-11-07 12:07:22.357295', NULL),
(466, '2025-03-13', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:22.461367', '2025-11-07 12:07:22.461383', NULL),
(467, '2025-08-13', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:22.553600', '2025-11-07 12:07:22.553618', NULL),
(468, '2025-09-13', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:22.676371', '2025-11-07 12:07:22.676390', NULL),
(469, '2025-10-13', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:22.777149', '2025-11-07 12:07:22.777166', NULL),
(470, '2024-11-13', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"40\", \"employee_name\": \"Kumar\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:22.864543', '2025-11-07 12:07:22.864562', NULL),
(471, '2024-12-13', '[{\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:22.929706', '2025-11-07 12:07:22.929720', NULL),
(472, '2025-01-14', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:23.022931', '2025-11-07 12:07:23.022949', NULL),
(473, '2025-02-14', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:23.118712', '2025-11-07 12:07:23.118729', NULL),
(474, '2025-03-14', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"50\", \"employee_name\": \"Guru\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:23.240889', '2025-11-07 12:07:23.240907', NULL),
(475, '2025-04-14', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 0, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:23.331120', '2025-11-07 12:07:23.331138', NULL),
(476, '2025-05-14', '[{\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:23.444529', '2025-11-07 12:07:23.444549', NULL),
(477, '2025-07-14', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:23.539639', '2025-11-07 12:07:23.539659', NULL),
(478, '2025-08-14', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:23.638949', '2025-11-07 12:07:23.638968', NULL);
INSERT INTO `xe_attendance_records` (`id`, `date`, `attendance_data`, `created_at`, `last_updated`, `created_by_id`) VALUES
(479, '2025-10-14', '[{\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:23.753832', '2025-11-07 12:07:23.753851', NULL),
(480, '2024-11-14', '[{\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"40\", \"employee_name\": \"Kumar\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:23.853096', '2025-11-07 12:07:23.853115', NULL),
(481, '2025-01-15', '[{\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 0, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"40\", \"employee_name\": \"Kumar\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 0, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:23.973236', '2025-11-07 12:07:23.973254', NULL),
(482, '2025-02-15', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:24.070302', '2025-11-07 12:07:24.070322', NULL),
(483, '2025-03-15', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"50\", \"employee_name\": \"Guru\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:24.197066', '2025-11-07 12:07:24.197085', NULL),
(484, '2025-04-15', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 0, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:24.278220', '2025-11-07 12:07:24.278239', NULL),
(485, '2025-05-15', '[{\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 0, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:24.399566', '2025-11-07 12:07:24.399582', NULL),
(486, '2025-07-15', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:24.512467', '2025-11-07 12:07:24.512485', NULL),
(487, '2025-08-15', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:24.582828', '2025-11-07 12:07:24.582847', NULL),
(488, '2025-09-15', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:24.692714', '2025-11-07 12:07:24.692732', NULL),
(489, '2024-11-15', '[{\"employee_id\": \"40\", \"employee_name\": \"Kumar\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:24.797610', '2025-11-07 12:07:24.797637', NULL),
(490, '2025-01-16', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:24.901970', '2025-11-07 12:07:24.901986', NULL),
(491, '2025-04-16', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:24.972054', '2025-11-07 12:07:24.972070', NULL),
(492, '2025-05-16', '[{\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:25.087897', '2025-11-07 12:07:25.087914', NULL),
(493, '2025-06-16', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:25.174044', '2025-11-07 12:07:25.174062', NULL),
(494, '2025-07-16', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:25.275107', '2025-11-07 12:07:25.275125', NULL),
(495, '2025-08-16', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:25.369939', '2025-11-07 12:07:25.369959', NULL),
(496, '2025-09-16', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:25.483007', '2025-11-07 12:07:25.483025', NULL),
(497, '2025-10-16', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:25.588851', '2025-11-07 12:07:25.588870', NULL),
(498, '2024-11-16', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"40\", \"employee_name\": \"Kumar\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:25.698136', '2025-11-07 12:07:25.698153', NULL),
(499, '2024-12-16', '[{\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:25.811665', '2025-11-07 12:07:25.811683', NULL),
(500, '2025-01-17', '[{\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:25.920531', '2025-11-07 12:07:25.920549', NULL),
(501, '2025-02-17', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:26.021028', '2025-11-07 12:07:26.021046', NULL),
(502, '2025-03-17', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 0, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:26.134251', '2025-11-07 12:07:26.134269', NULL),
(503, '2025-04-17', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"39\", \"employee_name\": \"Julie\", \"status\": 0, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:26.248659', '2025-11-07 12:07:26.248678', NULL),
(504, '2025-05-17', '[{\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:26.366682', '2025-11-07 12:07:26.366701', NULL),
(505, '2025-06-17', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:26.444966', '2025-11-07 12:07:26.444985', NULL),
(506, '2024-10-17', '[{\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"55\", \"employee_name\": \"Nagarajan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:26.534654', '2025-11-07 12:07:26.534672', NULL),
(507, '2025-10-17', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:26.655664', '2025-11-07 12:07:26.655683', NULL),
(508, '2024-12-17', '[{\"employee_id\": \"50\", \"employee_name\": \"Guru\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:26.776097', '2025-11-07 12:07:26.776114', NULL),
(509, '2025-01-18', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:27.123958', '2025-11-07 12:07:27.123977', NULL),
(510, '2025-02-18', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:27.343863', '2025-11-07 12:07:27.343882', NULL),
(511, '2025-03-18', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:27.430696', '2025-11-07 12:07:27.430715', NULL),
(512, '2025-04-18', '[{\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"47\", \"employee_name\": \"Dev\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-04-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"39\", \"employee_name\": \"Julie\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:27.553578', '2025-11-07 12:07:27.553597', NULL),
(513, '2025-06-18', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:27.631152', '2025-11-07 12:07:27.631170', NULL),
(514, '2025-07-18', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:27.739852', '2025-11-07 12:07:27.739867', NULL),
(515, '2025-08-18', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:27.846204', '2025-11-07 12:07:27.846222', NULL),
(516, '2024-10-18', '[{\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:27.923862', '2025-11-07 12:07:27.923881', NULL),
(517, '2025-10-18', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:28.045753', '2025-11-07 12:07:28.045772', NULL),
(518, '2024-11-18', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:28.122590', '2025-11-07 12:07:28.122608', NULL),
(519, '2024-12-18', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:28.221304', '2025-11-07 12:07:28.221323', NULL),
(520, '2025-02-19', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:28.326374', '2025-11-07 12:07:28.326393', NULL),
(521, '2025-03-19', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:28.396098', '2025-11-07 12:07:28.396117', NULL),
(522, '2025-04-19', '[{\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"47\", \"employee_name\": \"Dev\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-04-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"39\", \"employee_name\": \"Julie\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:28.514023', '2025-11-07 12:07:28.514042', NULL),
(523, '2025-05-19', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:28.626468', '2025-11-07 12:07:28.626487', NULL),
(524, '2025-06-19', '[{\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"47\", \"employee_name\": \"Dev\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-04-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:28.716660', '2025-11-07 12:07:28.716678', NULL),
(525, '2025-07-19', '[{\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:28.831057', '2025-11-07 12:07:28.831072', NULL);
INSERT INTO `xe_attendance_records` (`id`, `date`, `attendance_data`, `created_at`, `last_updated`, `created_by_id`) VALUES
(526, '2025-08-19', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:28.946083', '2025-11-07 12:07:28.946101', NULL),
(527, '2025-09-19', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:29.062250', '2025-11-07 12:07:29.062267', NULL),
(528, '2024-11-19', '[{\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:29.147218', '2025-11-07 12:07:29.147236', NULL),
(529, '2024-12-19', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:29.240668', '2025-11-07 12:07:29.240687', NULL),
(530, '2025-02-20', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:29.324509', '2025-11-07 12:07:29.324528', NULL),
(531, '2025-03-20', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:29.391842', '2025-11-07 12:07:29.391861', NULL),
(532, '2025-05-20', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:29.490633', '2025-11-07 12:07:29.490652', NULL),
(533, '2025-06-20', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"49\", \"employee_name\": \"Soma Topno\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:29.619306', '2025-11-07 12:07:29.619325', NULL),
(534, '2025-08-20', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:29.737677', '2025-11-07 12:07:29.737698', NULL),
(535, '2025-09-20', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:29.854327', '2025-11-07 12:07:29.854345', NULL),
(536, '2024-11-20', '[{\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:29.932258', '2025-11-07 12:07:29.932277', NULL),
(537, '2024-12-20', '[{\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 0, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:30.037476', '2025-11-07 12:07:30.037495', NULL),
(538, '2025-01-21', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:30.126395', '2025-11-07 12:07:30.126414', NULL),
(539, '2025-02-21', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:30.216692', '2025-11-07 12:07:30.216711', NULL),
(540, '2025-03-21', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:30.324102', '2025-11-07 12:07:30.324120', NULL),
(541, '2025-04-21', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"48\", \"employee_name\": \"Sameer\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"47\", \"employee_name\": \"Dev\", \"status\": 0, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-04-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:30.431645', '2025-11-07 12:07:30.431664', NULL),
(542, '2025-05-21', '[{\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:30.532315', '2025-11-07 12:07:30.532333', NULL),
(543, '2025-06-21', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"49\", \"employee_name\": \"Soma Topno\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:30.664023', '2025-11-07 12:07:30.664042', NULL),
(544, '2025-07-21', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:30.795919', '2025-11-07 12:07:30.795937', NULL),
(545, '2025-08-21', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:30.905355', '2025-11-07 12:07:30.905371', NULL),
(546, '2024-11-21', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"40\", \"employee_name\": \"Kumar\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:31.012412', '2025-11-07 12:07:31.012431', NULL),
(547, '2024-12-21', '[{\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"50\", \"employee_name\": \"Guru\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 0, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:31.138615', '2025-11-07 12:07:31.138640', NULL),
(548, '2025-01-22', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:31.244543', '2025-11-07 12:07:31.244561', NULL),
(549, '2025-02-22', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:31.350858', '2025-11-07 12:07:31.350876', NULL),
(550, '2025-03-22', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:31.480137', '2025-11-07 12:07:31.480156', NULL),
(551, '2025-04-22', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"47\", \"employee_name\": \"Dev\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-04-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"48\", \"employee_name\": \"Sameer\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"39\", \"employee_name\": \"Julie\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:31.599267', '2025-11-07 12:07:31.599286', NULL),
(552, '2025-05-22', '[{\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:31.712262', '2025-11-07 12:07:31.712280', NULL),
(553, '2025-07-22', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:31.831586', '2025-11-07 12:07:31.831603', NULL),
(554, '2025-08-22', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:31.936431', '2025-11-07 12:07:31.936449', NULL),
(555, '2025-09-22', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:32.043239', '2025-11-07 12:07:32.043258', NULL),
(556, '2025-10-22', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 0, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 0, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0}]', '2025-11-07 12:07:32.151382', '2025-11-12 06:33:50.106233', NULL),
(557, '2024-11-22', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"40\", \"employee_name\": \"Kumar\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:32.256160', '2025-11-07 12:07:32.256175', NULL),
(558, '2025-01-23', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:32.360299', '2025-11-07 12:07:32.360314', NULL),
(559, '2025-04-23', '[{\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"47\", \"employee_name\": \"Dev\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-04-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"48\", \"employee_name\": \"Sameer\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"39\", \"employee_name\": \"Julie\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:32.499474', '2025-11-07 12:07:32.499492', NULL),
(560, '2025-05-23', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:32.600149', '2025-11-07 12:07:32.600167', NULL),
(561, '2025-06-23', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:32.675585', '2025-11-07 12:07:32.675604', NULL),
(562, '2025-07-23', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:32.800901', '2025-11-07 12:07:32.800918', NULL),
(563, '2025-08-23', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:32.903882', '2025-11-07 12:07:32.903901', NULL),
(564, '2025-09-23', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:33.020834', '2025-11-07 12:07:33.020849', NULL),
(565, '2025-10-23', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:33.128769', '2025-11-07 12:07:33.128788', NULL);
INSERT INTO `xe_attendance_records` (`id`, `date`, `attendance_data`, `created_at`, `last_updated`, `created_by_id`) VALUES
(566, '2024-11-23', '[{\"employee_id\": \"40\", \"employee_name\": \"Kumar\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:33.231274', '2025-11-07 12:07:33.231291', NULL),
(567, '2024-12-23', '[{\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:33.338884', '2025-11-07 12:07:33.338903', NULL),
(568, '2025-01-24', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:33.459679', '2025-11-07 12:07:33.459696', NULL),
(569, '2025-02-24', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:33.562189', '2025-11-07 12:07:33.562207', NULL),
(570, '2025-03-24', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:33.680347', '2025-11-07 12:07:33.680366', NULL),
(571, '2025-04-24', '[{\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"47\", \"employee_name\": \"Dev\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-04-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"48\", \"employee_name\": \"Sameer\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"39\", \"employee_name\": \"Julie\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:33.817502', '2025-11-07 12:07:33.817521', NULL),
(572, '2025-05-24', '[{\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:33.926079', '2025-11-07 12:07:33.926095', NULL),
(573, '2025-06-24', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:33.991884', '2025-11-07 12:07:33.991903', NULL),
(574, '2025-07-24', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:34.112528', '2025-11-07 12:07:34.112546', NULL),
(575, '2025-09-24', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:34.234319', '2025-11-07 12:07:34.234337', NULL),
(576, '2025-10-24', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:34.349085', '2025-11-07 12:07:34.349104', NULL),
(577, '2024-12-24', '[{\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 0, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:34.466609', '2025-11-07 12:07:34.466640', NULL),
(578, '2025-01-25', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 0, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:34.587401', '2025-11-07 12:07:34.587419', NULL),
(579, '2025-02-25', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:34.690087', '2025-11-07 12:07:34.690106', NULL),
(580, '2025-03-25', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:34.799903', '2025-11-07 12:07:34.799922', NULL),
(581, '2025-04-25', '[{\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"47\", \"employee_name\": \"Dev\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-04-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"39\", \"employee_name\": \"Julie\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"48\", \"employee_name\": \"Sameer\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:34.941383', '2025-11-07 12:07:34.941400', NULL),
(582, '2025-06-25', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:35.015288', '2025-11-07 12:07:35.015307', NULL),
(583, '2025-07-25', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:35.142143', '2025-11-07 12:07:35.142162', NULL),
(584, '2025-10-25', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:35.251140', '2025-11-07 12:07:35.251158', NULL),
(585, '2024-11-25', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:35.322452', '2025-11-07 12:07:35.322471', NULL),
(586, '2024-12-25', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:35.427168', '2025-11-07 12:07:35.427186', NULL),
(587, '2025-02-26', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:35.532755', '2025-11-07 12:07:35.532774', NULL),
(588, '2025-03-26', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:35.650292', '2025-11-07 12:07:35.650312', NULL),
(589, '2025-04-26', '[{\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"48\", \"employee_name\": \"Sameer\", \"status\": 0, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"47\", \"employee_name\": \"Dev\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-04-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"39\", \"employee_name\": \"Julie\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:35.789094', '2025-11-07 12:07:35.789113', NULL),
(590, '2025-05-26', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"49\", \"employee_name\": \"Soma Topno\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:35.929321', '2025-11-07 12:07:35.929340', NULL),
(591, '2025-06-26', '[{\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:36.014373', '2025-11-07 12:07:36.014390', NULL),
(592, '2025-07-26', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:36.129226', '2025-11-07 12:07:36.129245', NULL),
(593, '2025-08-26', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:36.241566', '2025-11-07 12:07:36.241584', NULL),
(594, '2025-09-26', '[{\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:36.378072', '2025-11-07 12:07:36.378091', NULL),
(595, '2024-11-26', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:36.484214', '2025-11-07 12:07:36.484233', NULL),
(596, '2024-12-26', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:36.641759', '2025-11-07 12:07:36.641778', NULL),
(597, '2025-01-27', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:36.782539', '2025-11-07 12:07:36.782555', NULL),
(598, '2025-02-27', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:36.937975', '2025-11-07 12:07:36.937994', NULL),
(599, '2025-03-27', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:37.049927', '2025-11-07 12:07:37.049945', NULL),
(600, '2025-04-27', '[{\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:37.125654', '2025-11-07 12:07:37.125674', NULL),
(601, '2025-05-27', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"49\", \"employee_name\": \"Soma Topno\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:37.267838', '2025-11-07 12:07:37.267856', NULL),
(602, '2025-06-27', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"33\", \"employee_name\": \"Deepavali\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:37.410184', '2025-11-07 12:07:37.410202', NULL),
(603, '2025-08-27', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:37.500614', '2025-11-07 12:07:37.500639', NULL);
INSERT INTO `xe_attendance_records` (`id`, `date`, `attendance_data`, `created_at`, `last_updated`, `created_by_id`) VALUES
(604, '2025-09-27', '[{\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:37.620082', '2025-11-07 12:07:37.620100', NULL),
(605, '2024-12-27', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 0, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:37.734066', '2025-11-07 12:07:37.734092', NULL),
(606, '2025-01-28', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 0, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:37.831946', '2025-11-07 12:07:37.831966', NULL),
(607, '2025-02-28', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:37.937270', '2025-11-07 12:07:37.937288', NULL),
(608, '2025-03-28', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:38.045336', '2025-11-07 12:07:38.045354', NULL),
(609, '2025-04-28', '[{\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"39\", \"employee_name\": \"Julie\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"42\", \"employee_name\": \"Lakshmi\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"38\", \"employee_name\": \"Anjali\", \"status\": 0, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"47\", \"employee_name\": \"Dev\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-04-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:38.182897', '2025-11-07 12:07:38.182917', NULL),
(610, '2025-05-28', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"49\", \"employee_name\": \"Soma Topno\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:38.317075', '2025-11-07 12:07:38.317091', NULL),
(611, '2025-06-28', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"33\", \"employee_name\": \"Deepavali\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:38.456224', '2025-11-07 12:07:38.456243', NULL),
(612, '2025-07-28', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:38.559253', '2025-11-07 12:07:38.559271', NULL),
(613, '2024-10-28', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 0, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:38.627428', '2025-11-07 12:07:38.627446', NULL),
(614, '2024-11-28', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:38.697512', '2025-11-07 12:07:38.697531', NULL),
(615, '2024-12-28', '[{\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:38.799886', '2025-11-07 12:07:38.799904', NULL),
(616, '2025-01-29', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:38.906273', '2025-11-07 12:07:38.906291', NULL),
(617, '2025-03-29', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:39.006042', '2025-11-07 12:07:39.006058', NULL),
(618, '2025-04-29', '[{\"employee_id\": \"38\", \"employee_name\": \"Anjali\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"47\", \"employee_name\": \"Dev\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-04-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"39\", \"employee_name\": \"Julie\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"48\", \"employee_name\": \"Sameer\", \"status\": 0, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"46\", \"employee_name\": \"Rajendhiran\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"42\", \"employee_name\": \"Lakshmi\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:39.165916', '2025-11-07 12:07:39.165935', NULL),
(619, '2025-05-29', '[{\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"49\", \"employee_name\": \"Soma Topno\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:39.301199', '2025-11-07 12:07:39.301217', NULL),
(620, '2025-07-29', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 0, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:39.418902', '2025-11-07 12:07:39.418919', NULL),
(621, '2024-10-29', '[{\"employee_id\": \"55\", \"employee_name\": \"Nagarajan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:39.507827', '2025-11-07 12:07:39.507845', NULL),
(622, '2024-11-29', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:39.574210', '2025-11-07 12:07:39.574226', NULL),
(623, '2025-01-30', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:39.680849', '2025-11-07 12:07:39.680864', NULL),
(624, '2025-04-30', '[{\"employee_id\": \"38\", \"employee_name\": \"Anjali\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"42\", \"employee_name\": \"Lakshmi\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"48\", \"employee_name\": \"Sameer\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:39.831959', '2025-11-07 12:07:39.831975', NULL),
(625, '2025-05-30', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"51\", \"employee_name\": \"Kalanjiyam\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"49\", \"employee_name\": \"Soma Topno\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:39.961885', '2025-11-07 12:07:39.961910', NULL),
(626, '2025-06-30', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"52\", \"employee_name\": \"Athi\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:40.079004', '2025-11-07 12:07:40.079022', NULL),
(627, '2025-07-30', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:40.183598', '2025-11-07 12:07:40.183617', NULL),
(628, '2024-10-30', '[{\"employee_id\": \"35\", \"employee_name\": \"Marimuthu\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:40.251190', '2025-11-07 12:07:40.251210', NULL),
(629, '2024-11-30', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:40.315185', '2025-11-07 12:07:40.315204', NULL),
(630, '2025-01-31', '[{\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 0, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:40.428728', '2025-11-07 12:07:40.428747', NULL),
(631, '2025-03-31', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:40.496416', '2025-11-07 12:07:40.496433', NULL),
(632, '2025-05-31', '[{\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"49\", \"employee_name\": \"Soma Topno\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}]', '2025-11-07 12:07:40.607829', '2025-11-07 12:07:40.607847', NULL),
(633, '2025-07-31', '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"status\": 1, \"wage_amount\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 0, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"44\", \"employee_name\": \"Murugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"status\": 1, \"wage_amount\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:40.727371', '2025-11-07 12:07:40.727389', NULL),
(634, '2024-12-31', '[{\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"status\": 1, \"wage_amount\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"status\": 1, \"wage_amount\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}]', '2025-11-07 12:07:40.825768', '2025-11-07 12:07:40.825782', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `xe_attendance_weekly_summary`
--

CREATE TABLE `xe_attendance_weekly_summary` (
  `id` bigint(20) NOT NULL,
  `week_start_date` date NOT NULL,
  `week_end_date` date NOT NULL,
  `total_employees` int(11) NOT NULL,
  `total_present_days` int(11) NOT NULL,
  `total_half_days` int(11) NOT NULL,
  `total_gross_wages` decimal(12,2) NOT NULL,
  `total_deductions` decimal(12,2) NOT NULL,
  `total_net_wages` decimal(12,2) NOT NULL,
  `total_paid_amount` decimal(12,2) NOT NULL,
  `total_pending_amount` decimal(12,2) NOT NULL,
  `is_wages_paid` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `xe_bill_images`
--

CREATE TABLE `xe_bill_images` (
  `id` bigint(20) NOT NULL,
  `image` varchar(500) NOT NULL,
  `original_filename` varchar(255) NOT NULL,
  `file_size` int(10) UNSIGNED DEFAULT NULL CHECK (`file_size` >= 0),
  `uploaded_at` datetime(6) NOT NULL,
  `yield_record_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `xe_crops`
--

CREATE TABLE `xe_crops` (
  `id` bigint(20) NOT NULL,
  `crop_name` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `crop_image` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `xe_crops`
--

INSERT INTO `xe_crops` (`id`, `crop_name`, `created_at`, `updated_at`, `crop_image`) VALUES
(3, 'lemon', '2025-10-30 13:04:06.026866', '2025-10-30 13:04:06.026928', 'crops/scaled_1000820225.jpg'),
(4, 'banana', '2025-10-30 13:04:53.521915', '2025-10-30 13:05:05.251325', 'crops/scaled_1000820231.jpg'),
(5, 'jackfruit', '2025-10-30 13:06:13.907854', '2025-10-30 13:06:13.907879', 'crops/scaled_1000820232.jpg'),
(6, 'pepper', '2025-10-30 13:06:26.411494', '2025-10-30 13:06:26.411524', ''),
(7, 'malai kaai banana', '2025-10-30 13:07:58.781723', '2025-10-30 13:07:58.781751', ''),
(8, 'elavam panju cotton', '2025-11-07 12:26:23.478741', '2025-11-07 12:26:23.478791', ''),
(9, 'coffee', '2025-11-07 12:31:52.100765', '2025-11-07 12:31:52.100822', ''),
(10, 'cashew', '2025-11-07 12:38:07.177848', '2025-11-07 12:38:07.177908', '');

-- --------------------------------------------------------

--
-- Table structure for table `xe_crop_variants`
--

CREATE TABLE `xe_crop_variants` (
  `id` bigint(20) NOT NULL,
  `crop_variant` varchar(100) NOT NULL,
  `unit` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `crop_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `xe_crop_variants`
--

INSERT INTO `xe_crop_variants` (`id`, `crop_variant`, `unit`, `created_at`, `updated_at`, `crop_id`) VALUES
(5, 'rasi', 'Pack', '2025-10-30 13:11:52.824057', '2025-10-30 13:11:52.824103', 3),
(6, 'chinna sillu', 'Pack', '2025-10-30 13:12:11.924394', '2025-10-30 13:12:11.924436', 3),
(7, 'periya sillu', 'Pack', '2025-10-30 13:12:30.510591', '2025-10-30 13:12:30.510614', 3),
(8, 'narthangai', 'Pack', '2025-10-30 13:12:54.714340', '2025-10-30 13:12:54.714365', 3),
(9, 'kalivu', 'Pack', '2025-10-30 13:13:09.203061', '2025-10-30 13:13:09.203119', 3),
(10, 'samburani', 'Bunch', '2025-10-30 13:13:46.258441', '2025-10-30 13:13:46.258463', 4),
(11, 'yelarasi', 'Bunch', '2025-10-30 13:13:57.143950', '2025-10-30 13:13:57.143977', 4),
(12, 'Malai - none', 'Pieces', '2025-10-30 13:31:27.941179', '2025-11-07 12:44:43.304317', 7),
(13, 'Jack - none', 'Pieces', '2025-10-30 13:31:40.898484', '2025-11-07 12:44:33.083099', 5),
(14, 'black', 'Pack', '2025-10-30 13:31:56.498491', '2025-10-30 13:31:56.498516', 6),
(15, 'white', 'Pack', '2025-10-30 13:32:24.020763', '2025-10-30 13:32:24.020810', 6),
(16, 'Coffee-none', 'Pack', '2025-11-07 12:36:43.675946', '2025-11-07 12:44:22.446464', 9),
(17, 'Cashew-none', 'Pack', '2025-11-07 12:38:28.250691', '2025-11-07 12:44:07.223557', 10),
(18, 'full contract', 'Pack', '2025-11-09 08:59:51.213464', '2025-11-09 08:59:51.213506', 8);

-- --------------------------------------------------------

--
-- Table structure for table `xe_employee`
--

CREATE TABLE `xe_employee` (
  `id` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `tamil_name` varchar(255) NOT NULL,
  `joining_date` date NOT NULL,
  `emp_type` varchar(100) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `image_url` varchar(500) DEFAULT NULL,
  `contact` varchar(20) DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `xe_employee`
--

INSERT INTO `xe_employee` (`id`, `name`, `tamil_name`, `joining_date`, `emp_type`, `gender`, `image_url`, `contact`, `status`, `created_at`, `updated_at`) VALUES
(31, 'Pitchai', 'பிச்சை', '2024-05-30', 'Regular', 'Male', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/employee_images%2F09d77af4-e26a-464a-b5a4-008df439ce2e.jpg?alt=media&token=2943643b-c42e-40bb-91f6-7438799f0682', '9999999999', 1, '2025-08-08 12:18:15.032868', '2025-11-07 10:38:46.203324'),
(32, 'Chinnammal', 'சின்னம்மாள்', '2024-05-31', 'Regular', 'Female', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/employee_images%2Ffe94241b-e3d5-43dd-9817-062e98c41dcf.jpg?alt=media&token=0d17d615-d8b6-4dc8-83ed-16f95d3032c5', '9999999999', 1, '2025-08-08 12:18:15.032868', '2025-11-07 10:38:52.491479'),
(33, 'Deepavali', 'தீபாவளி', '2025-06-27', 'Contract', 'Male', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/employee_images%2F61040789-0036-4cf1-985b-b2b776ea3d6f.jpg?alt=media&token=e6db08ca-59ac-4db0-998e-5cd4def246b3', '', 1, '2025-08-08 12:18:15.032868', '2025-11-07 10:38:58.558223'),
(34, 'Rebeka', 'ரெபெக்கா', '2025-05-26', 'Regular', 'Female', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/employee_images%2F2966fcba-3125-4c91-8b59-a90e9c410b2f.jpg?alt=media&token=422b36ef-f08d-4e4b-94a2-8eee47d36012', '', 1, '2025-08-08 12:18:15.032868', '2025-11-07 10:39:05.067200'),
(35, 'Marimuthu', 'மாரிமுத்து', '2024-10-14', 'Regular', 'Male', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/employee_images%2Fe645315e-5a99-459c-89b2-80a27cd4dbed.jpg?alt=media&token=f62260ba-ed06-4d14-83cf-ac3aaad57deb', '', 1, '2025-08-08 12:18:15.032868', '2025-11-07 10:39:09.275591'),
(36, 'Thirumurugan', 'திருமுருகன்', '2024-06-19', 'Contract', 'Male', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/employee_images%2F80d0b47b-2e55-4548-9a61-51a8869aa3fc.jpg?alt=media&token=56310168-e1af-4507-ad83-03392a3129c0', '', 1, '2025-08-08 12:18:15.032868', '2025-11-07 10:39:16.245470'),
(37, 'Mohan', 'மோகன்', '2024-06-19', 'Contract', 'Male', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/employee_images%2F68161394-a45f-4081-9456-a6e10b3d5282.jpg?alt=media&token=357d929d-2f14-4e10-af50-7a5ac45f9962', '', 1, '2025-08-08 12:18:15.032868', '2025-11-07 10:39:24.038357'),
(38, 'Anjali', 'அஞ்சலி', '2025-04-28', 'Contract', 'Female', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/employee_images%2F3d7daf1a-4024-404e-9190-da39144fca8b.jpg?alt=media&token=07ddfde9-1bb7-4afc-bcd2-d6f78660a409', '', 1, '2025-08-08 12:18:15.032868', '2025-11-07 10:39:28.659218'),
(39, 'Julie', 'ஜுலீ', '2025-02-24', 'Contract', 'Female', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/employee_images%2F1745672341108?alt=media&token=0339ce9a-1685-44e4-bd68-724658d02745', '', 1, '2025-08-08 12:18:15.032868', '2025-11-07 10:39:32.441333'),
(40, 'Kumar', 'குமார்', '2024-06-19', 'Contract', 'Male', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/employee_images%2F048e980c-c928-4a25-8bfe-22b46581d65b.jpg?alt=media&token=060d11bf-ef1a-4e84-895e-b44f18a08dfd', '', 1, '2025-08-08 12:18:15.032868', '2025-11-07 10:39:37.973278'),
(41, 'Banu', 'பானு', '2024-05-31', 'Regular', 'Female', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/employee_images%2F69986973-d53e-4b49-a244-d7ef4477efb5.jpg?alt=media&token=e3e0eb8a-61df-4407-b712-f7b4bd8344fc', '', 1, '2025-08-08 12:18:15.032868', '2025-08-08 11:51:13.122137'),
(42, 'Lakshmi', 'லக்ஷ்மி', '2025-04-28', 'Contract', 'Female', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/employee_images%2F6b9778cb-f0fa-435d-8910-4a2727c7bdd4.jpg?alt=media&token=3b0ae35d-7e59-4e4f-881b-d6354ed82b9c', '', 1, '2025-08-08 12:18:15.032868', '2025-11-07 10:39:43.259336'),
(43, 'Elliajar Tete', 'எலியாஜார் தேடே', '2025-05-26', 'Regular', 'Male', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/employee_images%2Fba10ee94-2203-4d2b-93a6-20219caf9e59.jpg?alt=media&token=b0a24af4-dfc4-448e-a4a0-eaa2e3d213bc', '', 1, '2025-08-08 12:18:15.032868', '2025-11-07 10:39:46.621662'),
(44, 'Murugan', 'முருகன்', '2024-06-19', 'Contract', 'Male', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/employee_images%2F1719656569027?alt=media&token=f99af6ea-9118-45c8-8f3f-046ae5d040b8', '', 1, '2025-08-08 12:18:15.032868', '2025-11-07 10:39:50.301988'),
(46, 'Rajendhiran', 'ராஜேந்திரன்', '2025-04-29', 'Contract', 'Male', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/employee_images%2F5e436c7a-38d9-47a8-8182-ac2afe38ed03.jpg?alt=media&token=5598437b-e088-4633-9403-561b8aa85175', '', 1, '2025-08-08 12:18:15.032868', '2025-11-07 10:39:54.988904'),
(47, 'Dev', 'தேவ்', '2025-02-24', 'Contract', 'Male', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/employee_images%2F1748687252852?alt=media&token=2de88527-5eaf-46c4-98ab-e311e836a161', '', 1, '2025-08-08 12:18:15.032868', '2025-11-07 10:39:58.379041'),
(48, 'Sameer', 'சமீர்', '2025-02-24', 'Contract', 'Male', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/employee_images%2F1748687279807?alt=media&token=57eefd18-9220-4d82-8908-0d32fde620fa', '', 1, '2025-08-08 12:18:15.032868', '2025-11-07 10:40:06.522805'),
(49, 'Soma Topno', 'சோமா டோப்னோ', '2025-05-26', 'Regular', 'Male', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/employee_images%2F61502456-9964-431d-bb41-63679f9d6165.jpg?alt=media&token=8c0b7fe2-00dc-475b-8eb5-8164d5103057', '', 1, '2025-08-08 12:18:15.032868', '2025-11-07 10:40:10.355087'),
(50, 'Guru', 'குரு', '2024-12-17', 'Contract', 'Male', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/employee_images%2Ff89c049f-bd4b-466d-91b3-90e870079ade.jpg?alt=media&token=97bce7d7-cff6-4779-8b91-29c83a094a52', '', 1, '2025-08-08 12:18:15.032868', '2025-11-07 10:40:15.283306'),
(51, 'Kalanjiyam', 'களஞ்சியம்', '2025-03-15', 'Regular', 'Male', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/employee_images%2F1748687467069?alt=media&token=92d32947-52b2-4cec-89fc-2b29efb37183', '', 1, '2025-08-08 12:18:15.032868', '2025-11-07 10:40:18.682504'),
(52, 'Athi', 'ஆதி', '2025-04-11', 'Regular', 'Male', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/employee_images%2F1748687485045?alt=media&token=4b450172-a04d-4e76-bbc8-293a8280b741', '', 1, '2025-08-08 12:18:15.032868', '2025-11-07 10:40:25.388168'),
(53, 'Nagesh', 'நாகேஷ்', '2024-05-31', 'Regular', 'Male', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/employee_images%2F11df89f7-8177-4439-a4b4-43fce58d2385.jpg?alt=media&token=6033f22f-a2d1-4aec-bb6a-d3fd6e0bee95', '9999999999', 1, '2025-08-08 12:18:15.032868', '2025-08-08 11:52:23.494181'),
(54, 'Iyappan', 'ஐயப்பன்', '2024-05-31', 'Regular', 'Male', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/employee_images%2Ff568809e-8841-498d-8a7e-d52acfe44b46.jpg?alt=media&token=29d3a23d-1ae3-4981-8a49-651205ae229c', '7904339743', 1, '2025-08-08 12:18:15.032868', '2025-08-08 11:52:34.570488'),
(55, 'Nagarajan', 'நாகராஜன்', '2024-06-29', 'Regular', 'Male', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/employee_images%2F7491f9c8-9fc5-4f01-8646-e7be9a382b05.jpg?alt=media&token=02e6e27b-64c4-4585-94a5-59e952eaf620', '7810040263', 1, '2025-08-08 12:18:15.032868', '2025-11-07 10:40:32.074970');

-- --------------------------------------------------------

--
-- Table structure for table `xe_expenses`
--

CREATE TABLE `xe_expenses` (
  `id` bigint(20) NOT NULL,
  `expense_name` varchar(255) NOT NULL,
  `date` date NOT NULL,
  `category` varchar(100) NOT NULL,
  `description` longtext DEFAULT NULL,
  `amount` decimal(12,2) NOT NULL,
  `spent_by` varchar(255) NOT NULL,
  `mode_of_payment` varchar(100) NOT NULL,
  `expense_image_url` varchar(500) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `xe_expenses`
--

INSERT INTO `xe_expenses` (`id`, `expense_name`, `date`, `category`, `description`, `amount`, `spent_by`, `mode_of_payment`, `expense_image_url`, `created_at`, `updated_at`) VALUES
(1, 'wages', '2025-06-01', 'Weekly Wages', NULL, 23600.00, 'leslie', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F6175bda2-5422-4e4c-a510-488ada012a3f.jpg?alt=media&token=a9adc228-06e8-4bd1-9061-e7d6297a2ba9', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(2, 'Driver Salary', '2024-07-17', 'Driver', NULL, 300.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fe3e4395c-21d8-4106-8f8d-7b4e24ce07f6.jpg?alt=media&token=3f7bae91-9dfc-4dab-82e7-895a9a677021', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(3, 'petrol', '2025-04-26', 'Fuel', 'bike petrol for. sirumalai visit', 500.00, 'leslie', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fd80ed1ae-8fdb-4cd7-ac40-8a56489eb963.jpg?alt=media&token=0f6fcb58-a36a-48c1-adc0-f84bae67b19d', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(4, 'rice kurunai for kumar', '2024-11-26', 'Miscellinious', NULL, 1080.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F24b83264-eafa-4a79-9ecd-026c20bfb3d7.jpg?alt=media&token=f4495523-48c7-4dbb-a18a-fb3c25f7035d', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(5, 'naathu', '2024-10-17', 'Tree Samplings', NULL, 22000.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F35b5ff30-62af-4da7-a26a-a4e5110cf6a8.jpg?alt=media&token=baa7a75f-65ea-4696-b2a7-0fb9fbb32994', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(6, 'aani, naatu vedi', '2025-01-09', 'Farm Maintenance', NULL, 1025.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fde982824-cc92-4fe5-aab0-f1ab9d6941cc.jpg?alt=media&token=3347bbaa-342b-44ee-b58d-794e84a8f09f', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(7, 'Driver Salary', '2024-07-15', 'Driver', NULL, 300.00, 'Leslie', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F71b317a2-08de-40e3-a02d-86763469316a.jpg?alt=media&token=71448586-07ce-4074-91c3-0dd78cf6aeda', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(8, 'Tree cutting labour ', '2024-10-20', 'Farm Maintenance', NULL, 11000.00, 'leslie', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F3b268ff9-7a9e-4c2e-9fc6-ec225f675d5a.jpg?alt=media&token=96956f33-a8db-4d1a-b9aa-5d24adee9aea', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(9, 'food and snacks', '2025-01-24', 'Food', 'for stay - saravanan', 300.00, 'saravana', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F9e85de61-f4a9-41e9-9299-c46df7dc753d.jpg?alt=media&token=62b181aa-70c8-4998-a177-5500ba639620', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(10, 'Wood Cutter', '2024-06-22', 'Farm Maintenance', NULL, 3000.00, 'Leslie', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F7cf6600e-61fe-466a-98f1-e76099f37941.jpg?alt=media&token=15cde564-3bc9-4d52-bb6e-15d072eac263', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(11, 'Tea', '2024-06-01', 'Food', 'One Parcel', 200.00, 'Gladen', 'Card', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fcaf01b38-fdf4-4fdd-9a75-8d9276ed5b28.jpg?alt=media&token=0258427a-124e-46b2-a10a-3db9380e1f01', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(12, 'Fuel', '2024-07-20', 'Transport', NULL, 1000.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F09972985-b92d-45de-af2d-8032f97725a1.jpg?alt=media&token=b702d714-bea4-43f3-868d-e555093f8746', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(13, 'murugan sons marriage ', '2025-01-27', 'Donation and Give Away', NULL, 200.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Faac2718a-773e-4bc7-a3cd-9b741eed8c2a.jpg?alt=media&token=4dd496cf-3685-41ca-9a52-5f8a37b8f4fc', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(14, 'wages', '2024-12-22', 'Weekly Wages', NULL, 12150.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fa2226730-c507-4691-b7dc-796a9af68c6f.jpg?alt=media&token=e1665297-37cb-4f41-b279-c397fa347d02', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(15, 'rope ', '2025-05-08', 'Miscellinious', 'nocchi rope for yielding vaalai mattai', 80.00, 'saravana', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F7b2982b2-ed06-4e7b-9117-f1145167c931.jpg?alt=media&token=19abffea-3ad0-40d3-8eb2-07c578406b53', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(16, 'wages', '2025-03-02', 'Weekly Wages', NULL, 20300.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F9b0d316b-2707-4e38-ba92-0c63cac2b7e4.jpg?alt=media&token=6afc25c2-3a39-49ba-bb7a-c0970dc5f64b', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(17, 'Wages', '2024-09-14', 'Weekly Wages', NULL, 13050.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Ffd3a56e6-c609-467f-87de-9ec7f564a4ed.jpg?alt=media&token=837a3009-f62c-4dcb-9d78-ebc80fe0e1d8', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(18, 'Diesel', '2024-08-16', 'Transport', NULL, 3000.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F6d59ef23-8147-447a-aace-1dbd385adf81.jpg?alt=media&token=e7101cc2-1d87-4d28-a238-25b198240ce4', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(19, 'Wages', '2024-07-07', 'Weekly Wages', NULL, 13650.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fd7b153de-bacc-43e5-80cf-bdf80b182a27.jpg?alt=media&token=14f8e78e-d738-4d74-a52e-fc35a542b0dc', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(20, 'Driver', '2024-07-20', 'Driver', NULL, 300.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F0971e271-ee2f-4245-bac2-93b75f2bcaf1.jpg?alt=media&token=60830d67-d66b-4847-8013-c3a998611c50', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(21, 'petrol', '2025-05-07', 'Fuel', 'petrol going sirumalai', 200.00, 'saravana', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F6e14dccf-79e9-4ff7-b67d-b5ce3b9a03f7.jpg?alt=media&token=68040542-544a-475b-9bb2-cfcae3188365', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(22, 'fuel', '2024-11-26', 'Fuel', NULL, 1000.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F177068a6-1434-47fb-a81b-28d7f924342c.jpg?alt=media&token=bcbe6f1a-9b08-4e85-9fcb-8a6b2fe4aab7', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(23, 'soup and bread omlet', '2025-01-04', 'Food', 'saravana and angya', 127.00, 'saravana', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F32aa8efe-451c-4753-a362-2d09accd1d09.jpg?alt=media&token=baf2cff6-141d-4281-97b9-c46db72c9d67', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(24, 'Driver Salary', '2024-06-29', 'Driver', NULL, 700.00, 'Leslie', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fbb7a85d2-b79b-4b0e-9ef3-bc08b6f18318.jpg?alt=media&token=d82bde9d-9f16-4fa7-bf24-7e7a0d369062', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(25, 'wages', '2024-10-06', 'Weekly Wages', NULL, 7200.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F1216d836-c981-4a61-94b4-9675c7cea03e.jpg?alt=media&token=96e6ed4b-1ff8-4d33-87bc-6efdfdb5a634', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(26, 'Food Mrg Aft', '2024-07-16', 'Food', NULL, 85.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F1435ea18-7978-41e2-b9b0-3d2013c0b0fb.jpg?alt=media&token=0ca1a340-dc3e-42eb-9785-b0af3039cb9f', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(27, 'jeep service', '2024-12-12', 'Jeep Maintenance', NULL, 2850.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fc9ce7c38-e44f-4929-84fb-e8d9e640adc4.jpg?alt=media&token=0d474975-bb04-49e2-8018-7564d7b19f1c', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(28, 'Diesel', '2024-06-09', 'Transport', 'Going Sirumalai', 1000.00, 'Leslie', 'Card', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fb1629014-a872-4a48-ac92-6b6cb7719f2f.jpg?alt=media&token=ac47cb82-d30c-4ad0-a09a-fc58fa617a45', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(29, 'Jeep Repair', '2024-05-28', 'Jeep Maintanence', 'Jeep Repair', 1400.00, 'Leslie', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F1717995298602?alt=media&token=262a9efe-2d85-4fed-9166-56fb4f50fec3', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(30, 'diesel', '2025-01-26', 'Fuel', NULL, 700.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F94fc243b-43b1-49c9-a6be-068c6e7c3359.jpg?alt=media&token=9ea7c27b-607c-49f1-bce7-97954ef16efd', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(31, 'saravana food expense for staying dgl', '2025-04-23', 'Food', 'saravana food advance', 500.00, 'leslie', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fb0b27959-0999-45f9-976f-586259127fde.jpg?alt=media&token=b4ee84db-6987-4777-a63c-65a2fac75e9c', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(32, 'wages', '2025-04-26', 'Weekly Wages', NULL, 21750.00, 'leslie', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fb7e3c7c5-c0e7-459b-bda9-043c12e3e21c.jpg?alt=media&token=aba996b7-558c-437a-8256-85de6c1dfedf', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(33, 'Fuel', '2024-07-15', 'Transport', NULL, 1000.00, 'Leslie', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F4e1c0bd8-9443-4270-b05d-21ce76ebfcde.jpg?alt=media&token=7548bd93-0dde-46e0-b300-1e108213f4b1', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(34, ' Wages', '2024-06-21', 'Weekly Wages', NULL, 18600.00, 'Leslie', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F78acd84c-e72f-482c-8a44-eca262624d93.jpg?alt=media&token=140a13ce-8a9e-4b49-ab89-32b36670fdfc', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(35, 'Groceries', '2024-05-31', 'Food', 'Groceries', 419.00, 'Leslie', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F3b4beb80-1914-438e-9fe2-7500e29212e7.jpg?alt=media&token=ccac1547-5453-4340-9b9a-8ea01c3b43f1', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(36, 'Petrol', '2024-06-05', 'Transport', 'Sirumalai Visit', 300.00, 'Leslie', 'UPI', 'nan', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(37, 'Breakfast And Tea', '2024-07-17', 'Food', NULL, 68.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F0bc01e18-9455-4fd4-b38d-510db285c8c2.jpg?alt=media&token=80ce3532-d7a5-4f8d-8c0c-317b6d394ae5', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(38, 'petrol', '2025-02-13', 'Fuel', NULL, 300.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F2a821933-421f-4f69-b836-bd3b43af3820.jpg?alt=media&token=af22d194-8885-4613-9620-4abca8a333fd', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(39, 'wages', '2025-05-18', 'Weekly Wages', NULL, 13700.00, 'leslie', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fe3aab369-6eb4-44fc-b058-f5ed7f9f9425.jpg?alt=media&token=1fcedf5b-77f4-494c-8723-1f6b291d8b5b', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(40, 'redbus', '2025-04-23', 'Transport', 'saravana chennai to dgl bus ticket', 500.00, 'leslie', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F1ae8ef34-903a-4e84-b933-c76c990b9545.jpg?alt=media&token=6a1546f6-ecea-4fc7-8e64-87d8fb64adc7', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(41, 'jeep cabin light change', '2024-11-26', 'Jeep Maintenance', NULL, 280.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F1f50862c-fe62-4953-942e-5b7639b8c525.jpg?alt=media&token=eaa915e0-7b3c-43df-bd0c-bb4a93514c6a', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(42, 'wages', '2025-05-25', 'Weekly Wages', NULL, 17800.00, 'leslie', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F16f3bfc7-1d8a-4739-b27d-fb4fe361716b.jpg?alt=media&token=5cd57f7c-b24a-4972-a117-c07df36a3d13', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(43, 'Diesel', '2024-09-26', 'Transport', NULL, 1500.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Ffb8645aa-7cc4-4f8f-8ec3-13690b63c1c2.jpg?alt=media&token=28f3b016-36f1-4df4-9656-58237698e0f8', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(44, 'eb - palaiyur house', '2024-10-26', 'EB/Phone/Admin EXP', NULL, 214.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F5d0c8d15-8da3-4832-8602-5f72fed503e8.jpg?alt=media&token=6a7f7786-347e-48e3-acee-50b2526736aa', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(45, 'wages', '2025-02-16', 'Weekly Wages', NULL, 6100.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F7fe9a124-bc41-49b2-9642-e2b0b48a4120.jpg?alt=media&token=8630d46e-1c17-43ba-bc11-bb8f61cadb44', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(46, 'wages', '2025-06-08', 'Weekly Wages', NULL, 13500.00, 'leslie', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F70e171ea-4f07-4cf8-a696-e0e4f6782373.jpg?alt=media&token=fb153cdb-d4a3-4779-97ad-51164a4f9bd5', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(47, 'petrol for motor ', '2025-04-09', 'Fuel', 'naathu thanni pachu motor petrol', 500.00, 'leslie', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F76ca5d83-8381-4f97-9511-886cce67733a.jpg?alt=media&token=6385744c-aa7a-4494-881a-59126d291fa3', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(48, 'contractor pending salary', '2024-10-20', 'Farm Maintenance', NULL, 30000.00, 'leslie', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F489198c9-62a4-4d41-8254-3cf0a71322f8.jpg?alt=media&token=dcb21791-21a6-4a9e-bce3-515359a37146', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(49, 'wages', '2025-05-11', 'Weekly Wages', NULL, 13700.00, 'leslie', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F5990f1e0-5cea-4a61-82f1-7cf376ec8998.jpg?alt=media&token=dc5c18a4-dc38-43d8-bda1-f3c0d0f1a9cd', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(50, 'Wages salary', '2024-09-28', 'Weekly Wages', NULL, 14700.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fc460a14b-1bad-4de0-af43-27e7c3c8e0e4.jpg?alt=media&token=4e8dbcbe-4848-454b-b941-a2abf5108ebb', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(51, 'grid veli and pardha', '2024-10-20', 'Farm Maintenance', NULL, 9200.00, 'leslie', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F92bf5c41-9bff-4e37-b3c8-a87ed76c08c5.jpg?alt=media&token=b7acd4bc-5313-41b3-a490-ff816bdb9573', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(52, 'food', '2025-05-07', 'Food', 'lunch ', 80.00, 'saravana', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fa8488021-31d6-406d-9f24-a0c5df35ac73.jpg?alt=media&token=3059e73d-6da4-4a8b-88ab-32171ddecae6', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(53, 'wages', '2025-01-19', 'Weekly Wages', NULL, 9500.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F74511904-d562-4117-8728-9308224c7c81.jpg?alt=media&token=a67b12ff-bf47-42bb-8cc9-7aad11fd773e', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(54, 'food', '2025-05-08', 'Food', 'lunch, biscuits', 50.00, 'saravana', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fb0dd32c5-cd92-41a3-8c34-0bc9f1a3e4dd.jpg?alt=media&token=e14bc901-41ac-4b05-8f82-066aa9650084', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(55, 'rice and vegetables', '2025-01-04', 'Food', NULL, 124.00, 'leslie', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F81e61824-80ce-418f-8275-0b87ba7a8759.jpg?alt=media&token=54363b39-1eda-47ba-bf24-397422fa701e', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(56, 'machine repair', '2024-09-13', 'Machine and Motor Repairs', NULL, 1250.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F6daae5a5-3550-4372-8b90-27961512c550.jpg?alt=media&token=90736e71-8304-4d78-94fd-3fff857718cd', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(57, 'Food', '2024-05-31', 'Food', 'Sweets', 880.00, 'Leslie', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F544799e1-6f5a-491f-8bc0-d18dc92b1998.jpg?alt=media&token=67aa1944-6fad-49cc-a5ae-8b421e54d4da', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(58, 'Food', '2024-05-31', 'Food', 'Chips', 150.00, 'Leslie', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F71cdbe6c-001b-4910-9073-eec1758abdd5.jpg?alt=media&token=48c436ab-4604-4033-bb03-dc61e31676d8', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(59, 'wages', '2024-11-10', 'Weekly Wages', NULL, 13500.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F0402e2ff-c096-4ed9-a9a3-284fe31e175a.jpg?alt=media&token=15b241ef-53b9-4f86-8169-f2dcefc9e721', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(60, 'fuel', '2024-11-10', 'Transport', NULL, 500.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F6dff15d1-8ba9-44e3-af93-faee41b17de6.jpg?alt=media&token=e5feccf4-6986-49f6-80e9-e5d9d3ccfb25', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(61, 'wages', '2024-11-17', 'Weekly Wages', NULL, 10800.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F5562b127-a438-494f-a5f3-2a1b52b2d31d.jpg?alt=media&token=92fc36ba-08ce-4625-b5f0-fcf0f9432df7', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(62, 'fuel', '2024-09-12', 'Transport', NULL, 1120.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fa308f3c9-6b3f-4b6a-97e0-0178bf0b9f78.jpg?alt=media&token=ed53d656-96ce-4cb2-8bdc-31e50169921d', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(63, 'milk and snacks', '2025-01-03', 'Food', 'milk, biscuit, bru and maggi for stay - saravanan', 145.00, 'saravana', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F398a3d2c-9697-4f03-92ed-a15e9ede71ad.jpg?alt=media&token=d45b6ae5-c4fe-4a05-b1b7-1d959a806408', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(64, 'Petrol', '2024-09-26', 'Transport', NULL, 200.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F09ae6054-7ac8-45bf-9daa-a64a6ebaea5b.jpg?alt=media&token=2396a71e-c35b-4ad7-9888-a01f9591c4ec', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(65, 'driver', '2024-11-20', 'Driver', 'mohan', 1500.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F4e5e74e6-84fd-475c-8176-4e9f14150400.jpg?alt=media&token=d6671461-7f90-4e78-a2ea-6cb45b137cdd', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(66, 'wages', '2025-01-11', 'Weekly Wages', NULL, 14250.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F6ee205ad-36dd-47c4-bcb4-74a7e4c12891.jpg?alt=media&token=d2793ae9-4af7-4632-afad-5b6516370865', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(67, 'Wages', '2024-08-31', 'Weekly Wages', NULL, 9075.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F3960e420-215a-4edd-81f5-4214ac16ab31.jpg?alt=media&token=6a02ca9d-981e-4649-80e9-cc89e3cbca70', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(68, 'wages', '2025-02-23', 'Weekly Wages', NULL, 12200.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F7489faf1-26d1-4bab-b172-6a2620c258c1.jpg?alt=media&token=9ae90a8c-ca0b-4296-9db1-6174b0364a7f', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(69, 'iyyappan advance', '2025-04-09', 'advance', 'iyyappan anna mothers treatment', 5000.00, 'leslie', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F1215fd63-6864-46c3-a7f6-43660f9f049c.jpg?alt=media&token=51f5c7b4-368b-4bcd-9d7b-63ccd409b1df', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(70, 'contract employees advance', '2024-10-01', 'Donation and Give Away', NULL, 1000.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F561dd81c-69f7-4dfe-954e-2951cb6e0039.jpg?alt=media&token=342b6543-90e9-40bf-a693-26df73865800', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(71, 'jeep spares and service', '2024-07-27', 'Jeep Maintenance', NULL, 5840.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F5c2b3240-20ce-4994-80d2-8f2a2123c598.jpg?alt=media&token=6fc47727-4884-4e0b-909d-ac97f1da5192', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(72, 'jeep repair', '2025-01-28', 'Jeep Maintenance', NULL, 1250.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F798ddc6b-5d2b-43b6-b3b4-2291e671209e.jpg?alt=media&token=aa88eb43-4cf4-4849-964f-c20c58df2887', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(73, 'naathu pai', '2024-11-11', 'Farm Maintenance', NULL, 340.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F030f26dd-8a8f-4694-a755-4cbcb4e69553.jpg?alt=media&token=88c40bfc-01be-46eb-8c68-44bab012aae3', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(74, 'water pump repair', '2024-11-12', 'Machine and Motor Repairs', NULL, 1823.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fff71edb6-eb86-4aad-8b3d-dd3f5d22a70f.jpg?alt=media&token=62880707-95c4-4c91-83d1-7c3bab71a269', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(75, 'Donation Thaalakadai', '2024-08-10', 'Donation and Give Away', NULL, 3000.00, 'Leslie', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fb9baa3de-2253-4e6c-ab4d-50197c0bc5c5.jpg?alt=media&token=1aea6edd-4f3b-40ba-97ad-9f2984deeec2', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(76, 'Wages', '2024-09-21', 'Weekly Wages', NULL, 9250.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F843a7d2f-0baf-49d1-ac17-88369580c142.jpg?alt=media&token=4079b48b-23e4-4056-a8b7-e5b1d616b390', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(77, 'food breakfast', '2024-11-10', 'Food', NULL, 120.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Feed7559b-365d-498e-a1d2-762dcca6b415.jpg?alt=media&token=8b70f029-0c64-4a26-bc2e-2732488a2ff8', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(78, 'recharge modem', '2024-09-27', 'EB/Phone/Admin EXP', NULL, 230.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fd4abebb1-1187-4dbc-9a1b-df65aef3d4b7.jpg?alt=media&token=cdcaea60-ce42-4db8-a2af-cd23c012e939', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(79, 'petrol', '2025-02-22', 'Fuel', '5 litres ', 500.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F06536a8c-f358-4c91-8192-9aa98ef5929b.jpg?alt=media&token=c4024b45-13f5-45eb-8713-40276101a630', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(80, 'petrol', '2024-09-03', 'Transport', NULL, 1000.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F9279926a-dd94-49c0-ae5a-ffc53e67bbd5.jpg?alt=media&token=19554d47-121d-480d-a651-f6052ad83115', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(81, 'Acting Driver Salary', '2024-06-15', 'Driver', 'Mohan Acting Driver ', 300.00, 'Leslie ', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fab73fa97-f1c6-4f65-adf4-bb2b8a8fc9ff.jpg?alt=media&token=bff24478-d96c-4fb0-9800-2e396000b1da', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(82, 'Employees Salary', '2024-06-08', 'Weekly Wages', NULL, 13950.00, 'Leslie', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fa367c4f8-8754-461f-8534-df87aef85841.jpg?alt=media&token=e8600395-a5dd-45d9-9118-9f1ca9708b52', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(83, 'Jeep Wiper', '2024-06-08', 'Jeep Maintanence', 'Changing Jeep Wiper', 290.00, 'Leslie', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fe01f63de-9e31-4d41-b6e3-23f1e5928575.jpg?alt=media&token=8765ab2b-a729-4def-8608-5b9d73cd398a', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(84, 'wages', '2025-01-04', 'Weekly Wages', NULL, 10800.00, 'leslie', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F1053a961-4601-41d0-9ed4-fce407c71391.jpg?alt=media&token=d53bef3c-0770-47a6-96be-3630ebe918de', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(85, 'wifi recharge', '2024-11-04', 'EB/Phone/Admin EXP', NULL, 800.00, 'leslie', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F114554a1-a5e0-4cfc-b1e2-65766edc80a3.jpg?alt=media&token=c0c80e5b-f412-4a1d-98ad-08cf8fde25bf', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(86, 'Diesel', '2024-08-10', 'Transport', NULL, 1000.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F2ac7271a-9c09-4336-95a9-d28f225e583c.jpg?alt=media&token=e5f6e1d0-e5d3-4ea7-a0e2-1063710bc161', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(87, 'new employee onboarding advance', '2025-05-23', 'advance', 'new employee onboarding - hindi ', 1200.00, 'leslie', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F4ebc31ca-d7f2-4945-b4c2-016d14fd87e4.jpg?alt=media&token=548a4b26-e7d0-438c-b5a2-141c6deb79ca', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(88, 'diesel and distilled water', '2025-03-16', 'Farm Maintenance', NULL, 2080.00, 'leslie', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Ffc1dd774-cad3-4bc0-aa72-452034e0cdc4.jpg?alt=media&token=5f4dc907-60af-4e41-839f-d25900fe665e', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(89, 'water tank (300 lt) ', '2024-11-12', 'Farm Maintenance', NULL, 1000.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F0c51c387-2e29-4247-9036-24e01b3e05e8.jpg?alt=media&token=182a0e46-a137-42ad-9863-0748c1abe703', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(90, 'Wages', '2024-08-17', 'Weekly Wages', NULL, 13400.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Ffde8b429-c070-46c8-b055-259ade6bc42c.jpg?alt=media&token=b21d9581-ff0e-4527-a4e1-b313bb2d8a3b', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(91, 'wages', '2024-11-24', 'Weekly Wages', NULL, 9600.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fc8c643e9-bcbb-41db-9a83-8c6ee29217d3.jpg?alt=media&token=9cfc8f2b-eed3-4f8f-94ef-62705052c964', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(92, 'Employee Wages', '2024-06-01', 'Weekly Wages', NULL, 1375.00, 'Leslie', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F8d7fc830-e4cf-47fc-9402-37779fe24a8c.jpg?alt=media&token=1ab77786-b860-461c-9d45-c9e8880f054d', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(93, 'nets(veli for picchai kottam) ', '2025-05-02', 'Farm Maintenance', 'valai ', 17000.00, 'leslie', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fb5d0a73c-b205-4baf-91ce-50a7e65c9aef.jpg?alt=media&token=c63948fe-f829-4282-bf43-f0f751a84c88', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(94, 'breakfast and lunch', '2025-01-03', 'Food', 'lunch for saravana', 178.00, 'saravana', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F3bd2d1a8-d6af-420a-ad4b-d3d72652a0f8.jpg?alt=media&token=8a1909f4-9c66-400c-86e1-8a214370a420', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(95, 'wages', '2025-01-25', 'Weekly Wages', NULL, 11900.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Ffd6226c6-366c-4e03-bb46-8a9f0e6b0d94.jpg?alt=media&token=9f9b5b09-d998-4885-8562-81af08375a5e', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(96, 'Food', '2024-07-15', 'Food', NULL, 150.00, 'Leslie', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F3fd04a91-bd96-4f4e-9422-87f33ee48e27.jpg?alt=media&token=fffb21cf-6e1a-415c-86a0-7ccc11b85b8d', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(97, 'wages', '2025-03-09', 'Weekly Wages', NULL, 6200.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F503e0ab5-dbae-4a32-8746-7d05e481f600.jpg?alt=media&token=34fb72cc-0824-4458-8188-b7e523676806', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(98, 'Nets ', '2024-06-27', 'Farm Maintanence', NULL, 11750.00, 'Leslie', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F591b92be-b073-4d97-8e87-0d59441f5589.jpg?alt=media&token=53e853de-2ebd-4d96-9352-4837be9968a7', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(99, 'petrol', '2025-05-08', 'Fuel', 'petrol went sirumalai', 200.00, 'saravana', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F6f2623d9-4402-45cd-be51-b40d6964ba08.jpg?alt=media&token=0985fda8-7686-4bac-8f52-f9bc9aac4d2a', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(100, 'fuel and distilled water', '2024-10-13', 'Transport', NULL, 1260.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F30602f2f-7c1e-4da9-bd02-60ead67c89cb.jpg?alt=media&token=e82feb4e-b568-4778-a9d3-fbaa29f684b7', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(101, 'wifi dongle recharge', '2025-01-28', 'Farm Maintenance', 'wifi recharge - jio', 320.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F5f3b91f6-ad9a-4949-bc5f-7f23455395fb.jpg?alt=media&token=fcf5a919-6e0a-4887-882c-d13a5844026f', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(102, 'Wages ', '2024-08-03', 'Weekly Wages', NULL, 14700.00, 'Leslie', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fc2faa34d-fb1f-48b2-a6e8-49010cce2e54.jpg?alt=media&token=768bb4c4-7d2a-498e-9326-33eb7af9da6b', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(103, 'Wages', '2024-07-20', 'Weekly Wages', NULL, 17000.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F7c6a7d27-f91e-44aa-9ed2-92b12527b6c1.jpg?alt=media&token=11abcce0-0dd6-4bdd-8fcd-3878594095b5', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(104, 'diesel', '2025-01-09', 'Fuel', '5 litres', 466.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fb2145184-37b0-48ba-8b97-0e71cdf73bb5.jpg?alt=media&token=7df447bb-464e-4bf3-b856-6bc10cccf8d4', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(105, 'gloves', '2025-01-07', 'Farm Maintenance', 'gloves for employees', 240.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fb0d34c72-19d2-4eb3-a166-208123af02fc.jpg?alt=media&token=3b6cdba5-a173-4366-9f31-398ff2fac231', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(106, 'food', '2024-09-12', 'Food', NULL, 650.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fc92de9c0-36e0-43ea-8954-13890d9f7755.jpg?alt=media&token=0b6346e3-edf1-491a-a32f-f8fdf5e30e67', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(107, 'wages', '2024-12-15', 'Weekly Wages', 'saravana', 5100.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F4c2e9582-e992-43e6-8e23-7b689f396d5a.jpg?alt=media&token=6016cb34-a58e-4ec3-a506-aad367e5b3d5', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(108, 'Fuel', '2024-07-16', 'Transport', NULL, 1000.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F40178202-cdbb-4249-b198-3b882d25e17c.jpg?alt=media&token=96187903-3f8a-42c9-ba5b-727613efb53b', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(109, 'Jeep Service', '2024-05-28', 'Farm Maintanence', 'Jeep Service', 5600.00, 'Leslie', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F89771909-1a0a-42cc-865c-3af30af9cd28.jpg?alt=media&token=e5ce69dd-63ed-46b7-ab70-0ee0a143d0eb', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(110, 'tax (palaiyur) ', '2025-06-10', 'Donation and Give Away', 'palaiyur vari', 4000.00, 'leslie', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F72853ea0-5143-4407-85cc-63f9f97141f1.jpg?alt=media&token=7f77d533-1f8d-4643-80be-fece1017fb26', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(111, 'Milk Biscuit Curd', '2024-07-16', 'Food', NULL, 95.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fd83b2826-53ec-47cd-938c-850e50d3a70a.jpg?alt=media&token=f0b3781c-a309-4737-b2b6-d25577064958', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(112, 'tape for fixing pipes', '2024-11-26', 'Machine and Motor Repairs', NULL, 520.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F22f8a196-fb31-46ae-9274-511727187192.jpg?alt=media&token=472b99a2-e492-42db-8732-2cb5905aa44b', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(113, 'Stationary Things', '2024-08-16', 'Miscellinious', NULL, 185.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F57e87c02-726c-441b-98c1-8cc11ebac00a.jpg?alt=media&token=f7b44fe9-6f1e-4fb2-ac63-5e3e563733c4', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(114, 'lunch', '2024-09-26', 'Food', 'lunch for vinoth, leslie, and saravana', 420.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fb4b42744-7f93-494c-aa90-561f4267399e.jpg?alt=media&token=87919f4b-9b59-4fae-999a-1f5fefa13e00', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(115, 'wages', '2024-12-01', 'Weekly Wages', NULL, 1000.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F14f8becc-8bc1-4f4f-9cd5-da515e334757.jpg?alt=media&token=8cc53989-0a02-48b3-bd86-006380ce1a15', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(116, 'Wages', '2024-08-10', 'Weekly Wages', NULL, 18300.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fc1b846aa-ae5d-4c41-8487-6ab35923dfb6.jpg?alt=media&token=44c24484-5a3d-4664-96c0-187e7f178d0e', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(117, 'wages', '2025-03-23', 'Weekly Wages', NULL, 6800.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F55dd4e83-9259-46cb-9a03-dfb0f2d79eec.jpg?alt=media&token=b700c6b0-4b3e-46b4-86e2-74b79066df77', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(118, 'wages', '2025-02-08', 'Weekly Wages', NULL, 11400.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F686d07d6-e885-4b7e-b656-0b78fd7b9958.jpg?alt=media&token=704d397a-36c9-4398-a30f-3ebc0b14a82d', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(119, 'Beakfast', '2024-06-09', 'Food', 'Tea And Biscuit', 110.00, 'Saravana', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F1445332d-b630-455b-9cb0-66811eb93667.jpg?alt=media&token=c67c4b36-1d1d-48d8-853d-fa5138eb0e9b', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(120, 'Food', '2024-05-31', 'Food', 'Vegetables', 99.00, 'Leslie', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fb6a33cf6-f681-49fc-9648-79d42cbc360c.jpg?alt=media&token=8c7be40d-0cbf-481e-b0c9-017308b60835', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(121, 'Jeep Sticker', '2024-05-31', 'Jeep Maintanence', 'Jeep Sticker', 400.00, 'Leslie', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F0b50498a-8d72-409b-9ee3-6d9172b38de8.jpg?alt=media&token=422eefef-34fc-44e3-969a-7fabef833c98', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(122, 'wages', '2024-10-12', 'Weekly Wages', NULL, 13800.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F6cefb8fd-788d-4a26-8808-4b552020e79b.jpg?alt=media&token=86b50e96-cb3b-4ff3-9059-6a395d0d3c54', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(123, 'Food', '2024-06-05', 'Food', 'Breakfast And Lunch For Person', 226.00, 'Leslie', 'UPI', 'nan', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(124, 'wages', '2025-03-16', 'Weekly Wages', NULL, 21400.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fc03b549d-566c-4a7b-a8e6-c51a733798db.jpg?alt=media&token=a44448f2-83aa-46eb-8a64-33a36def531b', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(125, 'wages', '2024-07-27', 'Weekly Wages', NULL, 19050.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fe8b65ce8-6ab2-4d15-a6cd-51a146c227ad.jpg?alt=media&token=d73409e1-29e9-4979-b171-5d10222e5f65', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(126, 'snacks and tea', '2024-12-09', 'Food', NULL, 412.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F54aba992-4049-47cf-a925-6e9c0bde2360.jpg?alt=media&token=19ea1de2-98d1-4e52-a00d-cf061f96bba0', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(127, 'diesel', '2024-11-12', 'Transport', NULL, 1000.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F47786066-ea17-4432-986c-c60e11238fb5.jpg?alt=media&token=f960c6bf-af39-47ac-8da4-08fa9ed13496', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(128, 'Wages', '2024-09-07', 'Weekly Wages', NULL, 16950.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fa0210d0b-31d0-401a-939e-f34675f28a02.jpg?alt=media&token=73d59402-1880-4dec-9961-09b5b41dd51a', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(129, 'wages', '2024-12-08', 'Weekly Wages', NULL, 10050.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F17ae6a61-002a-4d0c-a54a-5196578f4932.jpg?alt=media&token=3b98ffb2-30f3-4cdb-96df-9ba7577b79c2', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(130, 'Petrol', '2024-07-24', 'Transport', NULL, 300.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fe310509b-b666-43e0-87dd-6f23b32e214b.jpg?alt=media&token=ba0febcf-930d-4cf5-92a6-b8f54162b94b', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(131, 'Workshop', '2024-06-01', 'Jeep Maintenance', NULL, 500.00, 'Dtxdt', 'Card', 'nan', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(132, 'jeep repair', '2025-04-10', 'Jeep Maintenance', NULL, 30000.00, 'leslie', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F323df8da-3a88-4a14-8dc7-a57f81bc7348.jpg?alt=media&token=c872fcd2-b834-4255-81f7-b76f6459ae50', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(133, 'vegetables and rice', '2024-12-08', 'Food', 'for stay', 243.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F70b3c895-ea67-40aa-91bd-b4f330c2c25f.jpg?alt=media&token=18107afc-8690-4afb-802a-191acb98ddcc', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(134, 'milk and biscuit', '2024-11-10', 'Food', NULL, 70.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Ff773c0e4-4125-40a9-b28e-4a5e892e9011.jpg?alt=media&token=5ec2975d-5fb4-4c01-afeb-ce1c530b8e0a', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(135, 'Pipes', '2025-04-20', 'Farm Maintenance', 'pipes 100 ft', 2950.00, 'leslie', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F23ae371e-2210-4fe4-aebc-ed6a9dc2819b.jpg?alt=media&token=02f8f66f-861a-46f9-82bd-cd0b86f9a93e', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(136, 'Wages', '2024-07-13', 'Weekly Wages', NULL, 10500.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F33654864-0a93-4cac-a2bb-9a7dc70786e1.jpg?alt=media&token=e2804ae0-7710-43a0-ba21-c894a7b8254d', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(137, 'lunch', '2024-10-01', 'Food', NULL, 437.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fc1e21342-8dde-43ec-8ec2-dc07e346b8dd.jpg?alt=media&token=44a45373-9d89-4fda-8923-ad596981715b', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(138, 'Salary', '2024-08-24', 'Weekly Wages', NULL, 3750.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F18519772-8bd3-44c6-bb41-bda0998b24e0.jpg?alt=media&token=ee3c42db-52fa-453a-a30b-eff2d57c826c', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(139, 'kayiru', '2024-07-27', 'Farm Maintenance', NULL, 75.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fb567bed6-4037-4e18-9689-de995ab5d635.jpg?alt=media&token=03a22636-175c-4653-952e-fe392ff0e77a', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(140, 'Jeep Repair ', '2024-05-27', 'Jeep Maintanence', 'Jeep Spare And Services', 23438.00, 'Leslie', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F1a02d43e-b1d5-4bd7-b10a-9fcd15df122e.jpg?alt=media&token=62e83f92-d328-4161-8254-20cf4c76752b', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(141, 'petrol and food', '2024-09-01', 'Food', NULL, 450.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F49f5cb40-d932-4fce-82f8-13ade8690fc1.jpg?alt=media&token=6b07b65a-9c92-4040-9187-808b524323b4', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(142, 'Food', '2024-07-20', 'Food', NULL, 360.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F677fd565-721e-4fe7-ae74-0702aa9342c7.jpg?alt=media&token=3dc7bf1a-a36d-484a-98b0-a6f003f8cec5', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(143, 'veli and kambi', '2024-10-27', 'Farm Maintenance', NULL, 23850.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Ffad2a9ca-1208-41fc-b58b-0e27925e0a15.jpg?alt=media&token=fcefb3bc-61aa-4735-b1fb-7ca135e2eb8f', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(144, 'dip marundhu ', '2024-07-27', 'Farm Maintenance', NULL, 300.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F319fe3d8-049d-4888-a38d-da05c4122671.jpg?alt=media&token=56b5d116-f351-400e-82e1-645214c7825e', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(145, 'veli and kambi', '2024-08-16', 'Farm Maintenance', NULL, 17000.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F07ecfffe-ad96-4a3f-83ce-f542eb681d90.jpg?alt=media&token=4898e884-76fe-4d67-81ab-ed82767be85d', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(146, 'naathu periyakulam', '2024-08-16', 'Tree Samplings', NULL, 6100.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fcc894354-8a07-4426-8ddf-cdf66d1735ca.jpg?alt=media&token=ec1bfa6c-943d-43c6-8b1f-ca5f5bd5940b', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(147, 'diesel', '2024-11-10', 'Transport', NULL, 1000.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F2be4d175-94f8-44e1-9e4b-4719ee26b90c.jpg?alt=media&token=39f3b70c-f36b-460c-a8b2-228d1a56f383', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(148, 'Eb', '2024-07-02', 'EB/Phone/Admin EXP', NULL, 204.00, 'Leslie', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fcb37f0d8-1b47-4fb1-9a8b-f2952139d02d.jpg?alt=media&token=64253f5f-9897-431b-b15e-6b4c550b791e', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(149, 'contract employees advance', '2024-10-06', 'Donation and Give Away', NULL, 10000.00, 'leslie', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F7075e13d-5fc2-49b4-b491-0f54b3efd663.jpg?alt=media&token=3ad8849f-5e0d-4aca-8565-c6a258015dfe', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(150, 'petrol with oil', '2025-05-02', 'Fuel', 'grass cutting machine petrol', 480.00, 'saravana', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fb92d7734-b7de-49a8-b8f4-85c3241f01f2.jpg?alt=media&token=4e26c11f-c74e-47e4-a6c2-902ee0934694', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(151, 'wages', '2025-02-02', 'Weekly Wages', NULL, 14100.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F25cc2346-0140-4bb7-9676-5e1f2f94e76b.jpg?alt=media&token=d4ba29e5-35ea-47d1-9ff7-ef18fef90620', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(152, 'vandi vadagai ', '2025-06-08', 'Transport', 'veli export from dgl to sirumalai transport charges', 1500.00, 'leslie', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F1ca9582c-c497-4d82-9612-ca3635570ef0.jpg?alt=media&token=913200f1-500d-4552-90be-0190b154694a', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(153, 'milk ', '2024-09-26', 'Food', NULL, 92.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F13478710-10c0-4fbe-9264-a4f878635c05.jpg?alt=media&token=52a9cc5d-791c-4645-8d40-4d6017add419', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(154, 'contract employees advance ', '2024-10-12', 'Donation and Give Away', NULL, 4000.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F984bb26f-e494-4202-beb0-d888cff98981.jpg?alt=media&token=092e0f4d-1a57-4f85-bb60-c633aa9f4c02', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(155, 'wages', '2024-12-29', 'Weekly Wages', NULL, 14700.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fb14082bc-33cc-4ea9-b6df-8375c227d797.jpg?alt=media&token=fcc50c17-a4e8-4b06-ae77-826bca1a1d49', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(156, 'Employee Wages', '2024-06-15', 'Weekly Wages', 'Wages For All Employees June ', 7150.00, 'Leslie ', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F69937ea2-9127-4b40-997f-9c59a1e48cd6.jpg?alt=media&token=4605af09-9168-461c-a7d9-7a6ead9719f2', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(157, 'milk and snacks ', '2024-11-12', 'Food', NULL, 180.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F3551c6f7-a7f8-42a3-8f35-def5e5d9832e.jpg?alt=media&token=2055fe19-a945-495c-a365-f61a6681d54a', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000');
INSERT INTO `xe_expenses` (`id`, `expense_name`, `date`, `category`, `description`, `amount`, `spent_by`, `mode_of_payment`, `expense_image_url`, `created_at`, `updated_at`) VALUES
(158, 'wages ', '2024-10-15', 'Weekly Wages', NULL, 22800.00, '', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Ff4bbf7da-8ed4-4159-9405-e09b839e738f.jpg?alt=media&token=6093ecc9-34ae-4729-ab1a-86624e1bbcef', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(159, 'Saravanan Salary', '2024-07-09', 'EB/Phone/Admin EXP', 'Saravana Salary ', 5000.00, 'Leslie', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fe7ce1cae-aa64-4171-9db7-7d6f6a82a6c6.jpg?alt=media&token=2d15b041-a106-44d9-bb64-06dce7b35812', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(160, 'Plastic Items', '2024-06-27', 'Miscellinious', NULL, 910.00, 'Leslie', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fa4475a27-11bc-44ee-8192-21702fee037f.jpg?alt=media&token=0a8caa35-a785-482b-821b-eecf4d0abd12', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(161, 'food, tea and snacks', '2024-11-26', 'Food', NULL, 180.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F5dfa93d9-3ac7-4e27-a604-004690e078a0.jpg?alt=media&token=397d7c50-d11a-490e-9834-b33f495802c1', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(162, 'petrol', '2025-04-25', 'Fuel', 'petrol for grass cutting machine', 500.00, 'saravana', 'Cash', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2F506c8b6f-a7ed-4df1-9447-a6e294293598.jpg?alt=media&token=93302b6a-6a43-4486-9851-bcaced1d75eb', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(163, 'water and chips', '2024-09-26', 'Food', NULL, 230.00, '', 'UPI', 'https://firebasestorage.googleapis.com/v0/b/xeorganics.appspot.com/o/exp_images%2Fdb852e44-50a1-489d-b577-4c9481f8b2d3.jpg?alt=media&token=13332a82-0e95-487a-bae8-5d715f54ca9f', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000'),
(609, 'wages', '2025-06-15', 'Weekly Wages', '', 5000.00, 'leslie', 'Cash', '/media/expense_images/default_7f0cc056-efe6-4bdf-ac67-001b1da5f633.jpg', '2025-08-01 06:07:16.007696', '2025-08-01 06:07:16.007723'),
(610, 'wages', '2025-06-22', 'Weekly Wages', '', 9200.00, 'leslie', 'Cash', '/media/expense_images/default_cbc2b626-23e5-4bb8-93c4-624f7756fe63.jpg', '2025-08-01 06:07:57.683549', '2025-08-01 06:07:57.683579'),
(611, 'wages', '2025-06-29', 'Weekly Wages', '', 9750.00, 'leslie', 'Cash', '/media/expense_images/default_a3ea0a46-c719-4d1f-842e-a4fa2a84aabd.jpg', '2025-08-01 06:08:28.001728', '2025-08-01 06:08:28.001761'),
(612, 'wages', '2025-07-06', 'Weekly Wages', '', 20500.00, 'leslie', 'Cash', '/media/expense_images/default_c629130f-32f8-4c1c-bca4-ffc6caaa30f1.jpg', '2025-08-01 06:08:53.335767', '2025-08-01 06:08:53.335790'),
(613, 'wages', '2025-07-13', 'Weekly Wages', '', 10400.00, 'leslie', 'Cash', '/media/expense_images/default_eb4ba6aa-6976-4fc6-893c-419a17169e52.jpg', '2025-08-01 06:09:19.620412', '2025-08-01 06:09:19.620452'),
(614, 'wages', '2025-07-20', 'Weekly Wages', '', 12150.00, 'leslie', 'Cash', '/media/expense_images/default_748feece-3ff5-42e2-8680-6dfefa9b50d5.jpg', '2025-08-01 06:09:44.729515', '2025-08-01 06:09:44.729556'),
(615, 'wages', '2025-07-27', 'Weekly Wages', '', 20500.00, 'leslie', 'Cash', '/media/expense_images/default_d57ed6c9-aac2-445e-b76a-885ded5eaacf.jpg', '2025-08-01 06:10:21.066173', '2025-08-01 06:10:21.066197'),
(616, 'petrol', '2025-07-09', 'Fuel', 'petrol for bike visit sirumalai', 300.00, 'saravana', 'UPI', '/media/expense_images/b071884a-b6da-41c2-b68a-5c2ef789aed1.jpg', '2025-08-01 06:12:53.291424', '2025-08-01 06:19:24.328683'),
(617, 'diesel', '2025-07-09', 'Fuel', 'diesel for motor xe estate', 1000.00, 'saravana', 'UPI', '/media/expense_images/a35e5a9a-4fcd-4ac2-afc4-f451f8981b9b.jpg', '2025-08-01 06:13:35.245389', '2025-08-01 06:19:45.815550'),
(618, 'valai', '2025-07-10', 'Farm Maintenance', '', 4250.00, 'leslie', 'UPI', '/media/expense_images/68fd34b0-ac72-4150-b370-c6657910da44.jpg', '2025-08-01 06:24:49.606792', '2025-08-01 06:24:49.606827'),
(619, 'food', '2025-07-09', 'Food', '', 200.00, 'leslie', 'UPI', '/media/expense_images/default_e59192bc-2c99-4413-8658-1f61523ebe8b.jpg', '2025-08-01 06:27:08.132760', '2025-08-01 06:27:08.132806'),
(620, 'food', '2025-07-10', 'Food', '', 180.00, 'leslie', 'UPI', '/media/expense_images/default_9eb526c0-6d51-49fe-a173-368b3f38a973.jpg', '2025-08-01 06:27:27.475807', '2025-08-01 06:27:27.475831'),
(621, 'eb', '2025-07-14', 'Eb/Phone/Admin Exp', 'palaiyur eb', 351.00, 'leslie', 'UPI', '/media/expense_images/bd9f7c59-9335-420e-bb06-c1c4963cf726.jpg', '2025-08-01 06:29:05.850349', '2025-08-01 06:29:05.850384'),
(622, '1.5inch hose (vinayaga mills)', '2025-07-20', 'Farm Maintenance', '', 2400.00, 'leslie', 'UPI', '/media/expense_images/0c9e39b1-4f16-49a9-9ed8-eff4db15b3ff.jpg', '2025-08-01 06:30:36.671637', '2025-08-01 06:30:36.671664'),
(623, 'diesel motor spares', '2025-07-20', 'Machine and Motor Repairs', '', 500.00, 'leslie', 'UPI', '/media/expense_images/40a112e9-1aaa-4e5b-bf4f-bf27e61e2590.jpg', '2025-08-01 06:31:17.440372', '2025-08-01 06:31:17.440406'),
(624, 'iyyappan food', '2025-07-20', 'Food', '', 100.00, 'leslie', 'UPI', '/media/expense_images/default_861b85d2-68bc-4bec-bcd3-e889c58c22e9.jpg', '2025-08-01 06:31:41.824101', '2025-08-01 06:31:41.824144'),
(625, 'jeep painting', '2025-07-19', 'Jeep Maintenance', '', 5000.00, 'leslie', 'UPI', '/media/expense_images/default_00b67c97-52e6-417c-8402-93efbb79882d.jpg', '2025-08-01 06:32:37.719226', '2025-08-01 06:32:37.719294'),
(626, 'plastic crate chennai', '2025-07-17', 'Miscellinious', '', 1400.00, 'leslie anna amma', 'UPI', '/media/expense_images/default_f7474ae0-a0ad-4651-b97c-7b3e727a9050.jpg', '2025-08-01 06:34:10.328498', '2025-08-01 06:34:10.328529'),
(627, 'bus luggage charge', '2025-07-20', 'Transport', '', 500.00, 'leslie', 'UPI', '/media/expense_images/default_16b0874e-4fee-4482-a75b-48973ba1c942.jpg', '2025-08-01 06:34:39.296770', '2025-08-01 06:34:39.296833'),
(628, 'lathe work', '2025-07-22', 'Machine and Motor Repairs', '', 1200.00, 'leslie', 'UPI', '/media/expense_images/cb316ef4-815c-46a4-a15c-bcc48e42611b.jpg', '2025-08-01 06:36:29.934372', '2025-08-01 06:36:29.934403'),
(629, 'diesel pump engine, head nut spanner', '2025-07-23', 'Machine and Motor Repairs', '', 1170.00, 'leslie', 'UPI', '/media/expense_images/3c3987e6-a35a-42ba-afa1-3bae6e406ff6.jpg', '2025-08-01 06:37:45.671937', '2025-08-01 06:37:45.671973'),
(630, 'petrol + luggage charge', '2025-07-23', 'Transport', 'petrol + chennai luggage charges', 700.00, 'leslie', 'UPI', '/media/expense_images/default_2d11e4e1-971e-44c3-8f04-9fdd08da0d8e.jpg', '2025-08-01 06:38:40.427830', '2025-08-01 06:38:40.427859'),
(631, 'Farm Necessary things', '2025-07-24', 'Farm Maintenance', 'gas regulator, erumbu powder, cycle tube, keep top rexin, petrol, food and snacks', 4000.00, 'leslie', 'UPI', '/media/expense_images/57d300b1-b326-4ada-963c-ca728f547827.jpg', '2025-08-01 06:40:33.330143', '2025-08-01 06:41:51.010280'),
(632, 'jeep rexin apex work', '2025-08-06', 'Jeep Maintenance', 'tailor charges', 3000.00, 'leslie', 'UPI', '/media/expense_images/default_312cc2c4-5fee-4c7e-8931-2de742e6f695.jpg', '2025-08-09 16:03:44.747438', '2025-08-09 16:03:44.747473'),
(633, 'iyyappan wages', '2025-08-06', 'Weekly Wages', 'iyyappan wages paid for last week', 5000.00, 'leslie', 'UPI', '/media/expense_images/default_72afde36-9b94-4041-9016-d2e840283b7f.jpg', '2025-08-09 16:04:34.171608', '2025-08-09 16:04:34.171633'),
(657, 'petrol', '2025-08-12', 'Fuel', 'sirumalai visit 10 and 12th aug', 500.00, 'leslie', 'UPI', '/media/expense_images/default_a70ea418-c0e0-41c7-940e-f531f18b39a7.jpg', '2025-08-23 10:30:07.496938', '2025-08-23 10:30:07.496976'),
(658, 'jeep tinker', '2025-08-12', 'Jeep Maintenance', 'tinkering labour charge', 5000.00, 'leslie', 'UPI', '/media/expense_images/default_0f436713-0181-48d0-b97c-f66d6d33617a.jpg', '2025-08-23 10:30:52.828308', '2025-08-23 10:30:52.828349'),
(659, 'petrol', '2025-08-14', 'Fuel', 'sirumalai visit', 200.00, 'leslie', 'UPI', '/media/expense_images/default_406c5510-6bd7-4cbf-af07-94a258a99e05.jpg', '2025-08-23 10:31:23.846450', '2025-08-23 10:31:23.846476'),
(660, 'iyyappan wages', '2025-08-14', 'Weekly Wages', 'iyyappan machine running wages', 2500.00, 'leslie', 'UPI', '/media/expense_images/default_ad811aaa-e877-4497-b100-5043055db6fd.jpg', '2025-08-23 10:32:58.348742', '2025-08-23 10:32:58.348768'),
(661, 'aani and erumbu podi', '2025-08-17', 'Farm Maintenance', 'aani and erumbu podi', 720.00, 'iyyappan', 'UPI', '/media/expense_images/2757e517-ea81-4eb2-9014-171f40132ccf.jpg', '2025-08-23 10:34:52.578838', '2025-08-23 10:34:52.578875'),
(686, 'Weekly Wages - Week 2025-11-03', '2025-11-12', 'Weekly Wages', 'Bulk wage payment for week 2025-11-03 to 2025-11-09 (9 employees)', 13600.00, 'Admin', 'Cash', NULL, '2025-11-12 06:23:38.956506', '2025-11-12 06:23:38.956522');

-- --------------------------------------------------------

--
-- Table structure for table `xe_farm_scrapedevent`
--

CREATE TABLE `xe_farm_scrapedevent` (
  `id` bigint(20) NOT NULL,
  `event_id` varchar(255) NOT NULL,
  `source_platform` varchar(100) NOT NULL,
  `source_url` varchar(500) NOT NULL,
  `event_name` varchar(500) NOT NULL,
  `event_type` varchar(100) DEFAULT NULL,
  `event_category` varchar(100) DEFAULT NULL,
  `event_format` varchar(50) DEFAULT NULL,
  `event_status` varchar(50) NOT NULL,
  `recurrence` varchar(50) DEFAULT NULL,
  `start_datetime` datetime(6) DEFAULT NULL,
  `end_datetime` datetime(6) DEFAULT NULL,
  `duration_minutes` int(11) DEFAULT NULL,
  `duration_iso` varchar(50) DEFAULT NULL,
  `registration_open` datetime(6) DEFAULT NULL,
  `registration_close` datetime(6) DEFAULT NULL,
  `submission_deadline` datetime(6) DEFAULT NULL,
  `venue_name` varchar(300) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `venue_capacity` int(11) DEFAULT NULL,
  `registration_fee` decimal(10,2) DEFAULT NULL,
  `currency` varchar(10) DEFAULT NULL,
  `sponsors` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`sponsors`)),
  `partners` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`partners`)),
  `tags` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`tags`)),
  `organiser_name` varchar(300) DEFAULT NULL,
  `organiser_contact_email` varchar(254) DEFAULT NULL,
  `organiser_contact_phone` varchar(50) DEFAULT NULL,
  `organiser_location_country` varchar(100) DEFAULT NULL,
  `target_audience` longtext DEFAULT NULL,
  `eligibility_criteria` longtext DEFAULT NULL,
  `language` varchar(10) NOT NULL,
  `agenda_link` varchar(500) DEFAULT NULL,
  `post_event_materials_link` varchar(500) DEFAULT NULL,
  `expected_attendance` int(11) DEFAULT NULL,
  `registration_url` varchar(500) DEFAULT NULL,
  `last_updated` datetime(6) NOT NULL,
  `notes` longtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `xe_jobs`
--

CREATE TABLE `xe_jobs` (
  `id` bigint(20) NOT NULL,
  `job_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `job_date` date NOT NULL,
  `job_status` varchar(20) NOT NULL,
  `no_of_employees` int(10) UNSIGNED NOT NULL CHECK (`no_of_employees` >= 0),
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `xe_job_employees`
--

CREATE TABLE `xe_job_employees` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `employee_id` bigint(20) NOT NULL,
  `job_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `xe_job_farm_segments`
--

CREATE TABLE `xe_job_farm_segments` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `farm_segment_id` bigint(20) NOT NULL,
  `job_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `xe_merchant`
--

CREATE TABLE `xe_merchant` (
  `id` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `address` longtext NOT NULL,
  `payment_terms` varchar(100) NOT NULL,
  `contact` varchar(15) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `xe_merchant`
--

INSERT INTO `xe_merchant` (`id`, `name`, `address`, `payment_terms`, `contact`, `created_at`, `updated_at`) VALUES
(1, 'msr', 'sirumalai shed', 'Cash', '7875494545', '2025-10-28 12:44:08.457476', '2025-11-09 09:37:27.140711'),
(2, 'iyyappan contract', 'thalakadai', 'UPI', '7904339743', '2025-11-09 09:34:57.067951', '2025-11-09 09:34:57.068007'),
(3, 'thangavel brothers', 'ottanchathiram', 'Cash', '9842140397', '2025-11-09 09:35:38.072762', '2025-11-09 09:35:38.072814'),
(4, 'SRJ commission mandi', 'sirumalai shed', 'Cash', '9944285996', '2025-11-09 09:36:19.669727', '2025-11-09 09:36:19.669782'),
(5, 'Palayur merchant coffee', 'palayur', 'Cash', '9898989999', '2025-11-09 09:37:03.580615', '2025-11-09 09:37:03.580649');

-- --------------------------------------------------------

--
-- Table structure for table `xe_payment_history`
--

CREATE TABLE `xe_payment_history` (
  `id` bigint(20) NOT NULL,
  `payment_amount` decimal(12,2) NOT NULL,
  `payment_date` datetime(6) NOT NULL,
  `payment_method` varchar(20) NOT NULL,
  `payment_reference` varchar(100) DEFAULT NULL,
  `notes` longtext DEFAULT NULL,
  `created_by` varchar(100) DEFAULT NULL,
  `sale_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `xe_sales`
--

CREATE TABLE `xe_sales` (
  `id` bigint(20) NOT NULL,
  `payment_mode` varchar(20) NOT NULL,
  `harvest_date` datetime NOT NULL,
  `bill_url` varchar(500) DEFAULT NULL,
  `total_amount` decimal(12,2) NOT NULL,
  `commission` decimal(12,2) NOT NULL,
  `lorry_rent` decimal(12,2) NOT NULL,
  `cooly_charges` decimal(12,2) NOT NULL,
  `total_deductions` decimal(12,2) NOT NULL,
  `total_calculated_amount` decimal(12,2) NOT NULL,
  `final_amount` decimal(12,2) NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `merchant_id` bigint(20) NOT NULL,
  `yield_record_id` bigint(20) NOT NULL,
  `paid_amount` decimal(12,2) NOT NULL,
  `payment_status` varchar(20) NOT NULL,
  `pending_amount` decimal(12,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `xe_sales`
--

INSERT INTO `xe_sales` (`id`, `payment_mode`, `harvest_date`, `bill_url`, `total_amount`, `commission`, `lorry_rent`, `cooly_charges`, `total_deductions`, `total_calculated_amount`, `final_amount`, `status`, `created_at`, `updated_at`, `merchant_id`, `yield_record_id`, `paid_amount`, `payment_status`, `pending_amount`) VALUES
(97, 'Cash', '2024-11-11 00:00:00', NULL, 9680.00, 1180.00, 0.00, 0.00, 1180.00, 10860.00, 9680.00, 'pending', '2025-11-10 14:04:25.437579', '2025-11-10 14:04:25.437594', 1, 206, 0.00, 'pending', 9680.00),
(98, 'Cash', '2025-03-23 00:00:00', NULL, 3600.00, 1400.00, 0.00, 0.00, 1400.00, 5000.00, 3600.00, 'pending', '2025-11-10 14:04:25.533408', '2025-11-10 14:04:25.533418', 4, 288, 0.00, 'pending', 3600.00),
(99, 'Cash', '2024-08-13 00:00:00', NULL, 5083.00, 0.00, 0.00, 0.00, 0.00, 5083.00, 5083.00, 'pending', '2025-11-10 14:04:25.619649', '2025-11-10 14:04:25.619659', 1, 270, 0.00, 'pending', 5083.00),
(100, 'Cash', '2025-03-16 00:00:00', NULL, 8840.00, 2261.00, 0.00, 0.00, 2261.00, 11101.00, 8840.00, 'pending', '2025-11-10 14:04:25.704335', '2025-11-10 14:04:25.704346', 4, 275, 0.00, 'pending', 8840.00),
(101, 'Cash', '2025-08-04 00:00:00', NULL, 1290.00, 162.00, 50.00, 10.00, 222.00, 1512.00, 1290.00, 'pending', '2025-11-10 14:04:25.791116', '2025-11-10 14:04:25.791127', 1, 228, 0.00, 'pending', 1290.00),
(102, 'Cash', '2024-08-14 00:00:00', NULL, 5888.00, 0.00, 0.00, 0.00, 0.00, 5888.00, 5888.00, 'pending', '2025-11-10 14:04:25.871090', '2025-11-10 14:04:25.871100', 1, 223, 0.00, 'pending', 5888.00),
(103, 'Cash', '2025-04-27 00:00:00', NULL, 8170.00, 1000.00, 800.00, 30.00, 1830.00, 10000.00, 8170.00, 'pending', '2025-11-10 14:04:25.951176', '2025-11-10 14:04:25.951185', 4, 239, 0.00, 'pending', 8170.00),
(104, 'Cash', '2025-04-12 09:31:00', NULL, 6880.00, 2320.00, 0.00, 0.00, 2320.00, 9200.00, 6880.00, 'pending', '2025-11-10 14:04:26.036195', '2025-11-10 14:04:26.036205', 4, 260, 0.00, 'pending', 6880.00),
(105, 'Cash', '2024-10-07 00:00:00', NULL, 5250.00, 0.00, 0.00, 0.00, 0.00, 3325.00, 3325.00, 'pending', '2025-11-10 14:04:26.114633', '2025-11-10 14:04:26.114644', 1, 247, 0.00, 'pending', 3325.00),
(106, 'Cash', '2025-04-20 00:00:00', NULL, 9560.00, 1190.00, 1100.00, 50.00, 2340.00, 11900.00, 9560.00, 'pending', '2025-11-10 14:04:26.247365', '2025-11-10 14:04:26.247375', 4, 266, 0.00, 'pending', 9560.00),
(107, 'Cash', '2025-01-06 00:00:00', NULL, 2140.00, 260.00, 0.00, 0.00, 260.00, 2400.00, 2140.00, 'pending', '2025-11-10 14:04:26.328615', '2025-11-10 14:04:26.328626', 1, 237, 0.00, 'pending', 2140.00),
(108, 'Cash', '2025-07-03 00:00:00', NULL, 2530.00, 420.00, 500.00, 30.00, 950.00, 3480.00, 2530.00, 'pending', '2025-11-10 14:04:26.409302', '2025-11-10 14:04:26.409313', 1, 283, 0.00, 'pending', 2530.00),
(109, 'Cash', '2025-07-24 00:00:00', NULL, 5150.00, 1800.00, 908.00, 80.00, 2788.00, 7938.00, 5150.00, 'pending', '2025-11-10 14:04:26.485951', '2025-11-10 14:04:26.485961', 1, 267, 0.00, 'pending', 5150.00),
(110, 'Cash', '2025-04-10 00:00:00', NULL, 2070.00, 320.00, 800.00, 42.00, 1162.00, 3232.00, 2070.00, 'pending', '2025-11-10 14:04:26.570845', '2025-11-10 14:04:26.570855', 1, 282, 0.00, 'pending', 2070.00),
(111, 'Cash', '2025-05-19 00:00:00', NULL, 3030.00, 340.00, 0.00, 30.00, 370.00, 3400.00, 3030.00, 'pending', '2025-11-10 14:04:26.642429', '2025-11-10 14:04:26.642439', 1, 251, 0.00, 'pending', 3030.00),
(112, 'Cash', '2024-12-04 00:00:00', NULL, 5890.00, 2710.00, 0.00, 0.00, 2710.00, 8600.00, 5890.00, 'pending', '2025-11-10 14:04:26.715655', '2025-11-10 14:04:26.715666', 4, 219, 0.00, 'pending', 5890.00),
(113, 'Cash', '2024-06-06 00:00:00', NULL, 3571.00, 109.00, 0.00, 0.00, 109.00, 3680.00, 3571.00, 'pending', '2025-11-10 14:04:26.802196', '2025-11-10 14:04:26.802207', 1, 205, 0.00, 'pending', 3571.00),
(114, 'Cash', '2024-06-28 00:00:00', NULL, 5150.00, 350.00, 0.00, 0.00, 350.00, 5500.00, 5150.00, 'pending', '2025-11-10 14:04:26.871167', '2025-11-10 14:04:26.871176', 1, 213, 0.00, 'pending', 5150.00),
(115, 'Cash', '2024-07-24 00:00:00', NULL, 3661.00, 65.00, 0.00, 0.00, 65.00, 3726.00, 3661.00, 'pending', '2025-11-10 14:04:26.937291', '2025-11-10 14:04:26.937300', 1, 214, 0.00, 'pending', 3661.00),
(116, 'Cash', '2025-04-25 00:00:00', NULL, 2680.00, 410.00, 1000.00, 40.00, 1450.00, 4130.00, 2680.00, 'pending', '2025-11-10 14:04:27.019670', '2025-11-10 14:04:27.019687', 1, 261, 0.00, 'pending', 2680.00),
(117, 'Cash', '2025-04-25 09:28:00', NULL, 2320.00, 330.00, 750.00, 18.00, 1098.00, 3418.00, 2320.00, 'pending', '2025-11-10 14:04:27.099307', '2025-11-10 14:04:27.099317', 1, 255, 0.00, 'pending', 2320.00),
(118, 'Cash', '2024-07-24 00:00:00', NULL, 2800.00, 0.00, 0.00, 0.00, 0.00, 2800.00, 2800.00, 'pending', '2025-11-10 14:04:27.173017', '2025-11-10 14:04:27.173026', 1, 258, 0.00, 'pending', 2800.00),
(119, 'Cash', '2024-07-19 00:00:00', NULL, 2600.00, 0.00, 0.00, 0.00, 0.00, 2600.00, 2600.00, 'pending', '2025-11-10 14:04:27.306414', '2025-11-10 14:04:27.306424', 1, 217, 0.00, 'pending', 2600.00),
(120, 'Cash', '2025-05-04 00:00:00', NULL, 9100.00, 1080.00, 600.00, 20.00, 1700.00, 10800.00, 9100.00, 'pending', '2025-11-10 14:04:27.392141', '2025-11-10 14:04:27.392151', 4, 216, 0.00, 'pending', 9100.00),
(121, 'Cash', '2025-05-25 00:00:00', NULL, 2100.00, 266.00, 300.00, 10.00, 576.00, 2676.00, 2100.00, 'pending', '2025-11-10 14:04:27.475639', '2025-11-10 14:04:27.475650', 1, 254, 0.00, 'pending', 2100.00),
(122, 'Cash', '2025-01-19 00:00:00', NULL, 6412.00, 2588.00, 0.00, 0.00, 2588.00, 9000.00, 6412.00, 'pending', '2025-11-10 14:04:27.558134', '2025-11-10 14:04:27.558143', 3, 229, 0.00, 'pending', 6412.00),
(123, 'Cash', '2025-03-09 00:00:00', NULL, 2230.00, 770.00, 0.00, 0.00, 770.00, 3000.00, 2230.00, 'pending', '2025-11-10 14:04:27.638435', '2025-11-10 14:04:27.638445', 1, 208, 0.00, 'pending', 2230.00),
(124, 'Cash', '2025-09-14 00:00:00', NULL, 4925.00, 675.00, 1100.00, 50.00, 1825.00, 6750.00, 4925.00, 'pending', '2025-11-10 14:04:27.712316', '2025-11-10 14:04:27.712327', 4, 291, 0.00, 'pending', 4925.00),
(125, 'Cash', '2025-08-04 00:00:00', NULL, 2368.00, 295.00, 480.00, 25.00, 800.00, 3168.00, 2368.00, 'pending', '2025-11-10 14:04:27.789003', '2025-11-10 14:04:27.789013', 1, 264, 0.00, 'pending', 2368.00),
(126, 'Cash', '2025-07-20 00:00:00', NULL, 845.00, 175.00, 700.00, 30.00, 905.00, 1750.00, 845.00, 'pending', '2025-11-10 14:04:27.862854', '2025-11-10 14:04:27.862864', 4, 227, 0.00, 'pending', 845.00),
(127, 'Cash', '2025-07-18 00:00:00', NULL, 1035.00, 115.00, 0.00, 0.00, 115.00, 1150.00, 1035.00, 'pending', '2025-11-10 14:04:27.940842', '2025-11-10 14:04:27.940853', 4, 256, 0.00, 'pending', 1035.00),
(128, 'Cash', '2024-12-18 00:00:00', NULL, 11239.00, 4079.00, 0.00, 0.00, 4079.00, 15318.00, 11239.00, 'pending', '2025-11-10 14:04:28.031831', '2025-11-10 14:04:28.031842', 3, 225, 0.00, 'pending', 11239.00),
(129, 'Cash', '2024-12-15 00:00:00', NULL, 2680.00, 720.00, 0.00, 0.00, 720.00, 3400.00, 2680.00, 'pending', '2025-11-10 14:04:28.126960', '2025-11-10 14:04:28.126970', 4, 243, 0.00, 'pending', 2680.00),
(130, 'Cash', '2024-12-08 00:00:00', NULL, 9855.00, 1153.00, 0.00, 0.00, 1153.00, 11008.00, 9855.00, 'pending', '2025-11-10 14:04:28.208991', '2025-11-10 14:04:28.209000', 3, 240, 0.00, 'pending', 9855.00),
(131, 'Cash', '2025-02-06 00:00:00', NULL, 2300.00, 850.00, 0.00, 0.00, 850.00, 3150.00, 2300.00, 'pending', '2025-11-10 14:04:28.288302', '2025-11-10 14:04:28.288311', 1, 250, 0.00, 'pending', 2300.00),
(132, 'Cash', '2025-06-25 00:00:00', NULL, 650.00, 0.00, 0.00, 0.00, 0.00, 650.00, 650.00, 'pending', '2025-11-10 14:04:28.370945', '2025-11-10 14:04:28.370955', 1, 278, 0.00, 'pending', 650.00),
(133, 'Cash', '2024-07-24 00:00:00', NULL, 1680.00, 0.00, 0.00, 0.00, 0.00, 1680.00, 1680.00, 'pending', '2025-11-10 14:04:28.449092', '2025-11-10 14:04:28.449102', 1, 235, 0.00, 'pending', 1680.00),
(134, 'Cash', '2025-03-25 00:00:00', NULL, 1935.00, 405.00, 0.00, 0.00, 405.00, 2340.00, 1935.00, 'pending', '2025-11-10 14:04:28.525957', '2025-11-10 14:04:28.525967', 1, 232, 0.00, 'pending', 1935.00),
(135, 'Cash', '2025-01-31 00:00:00', NULL, 5110.00, 2790.00, 0.00, 0.00, 2790.00, 7900.00, 5110.00, 'pending', '2025-11-10 14:04:28.601523', '2025-11-10 14:04:28.601533', 4, 274, 0.00, 'pending', 5110.00),
(136, 'Cash', '2024-11-06 00:00:00', NULL, 6710.00, 1890.00, 0.00, 0.00, 1890.00, 8600.00, 6710.00, 'pending', '2025-11-10 14:04:28.682209', '2025-11-10 14:04:28.682220', 4, 200, 0.00, 'pending', 6710.00),
(137, 'Cash', '2025-05-28 00:00:00', NULL, 3170.00, 639.00, 1500.00, 60.00, 2199.00, 5369.00, 3170.00, 'pending', '2025-11-10 14:04:28.755289', '2025-11-10 14:04:28.755299', 1, 202, 0.00, 'pending', 3170.00),
(138, 'Cash', '2024-11-17 00:00:00', NULL, 7310.00, 2090.00, 0.00, 0.00, 2090.00, 9400.00, 7310.00, 'pending', '2025-11-10 14:04:28.828834', '2025-11-10 14:04:28.828844', 4, 262, 0.00, 'pending', 7310.00),
(139, 'Cash', '2025-05-05 00:00:00', NULL, 1580.00, 200.00, 250.00, 20.00, 470.00, 2050.00, 1580.00, 'pending', '2025-11-10 14:04:28.908129', '2025-11-10 14:04:28.908139', 1, 249, 0.00, 'pending', 1580.00),
(140, 'Cash', '2025-01-10 00:00:00', NULL, 14477.00, 5300.00, 0.00, 0.00, 5300.00, 19777.00, 14477.00, 'pending', '2025-11-10 14:04:28.990139', '2025-11-10 14:04:28.990148', 3, 265, 0.00, 'pending', 14477.00),
(141, 'Cash', '2025-09-07 00:00:00', NULL, 7680.00, 970.00, 1000.00, 50.00, 2020.00, 9700.00, 7680.00, 'pending', '2025-11-10 14:04:29.077763', '2025-11-10 14:04:29.077774', 4, 230, 0.00, 'pending', 7680.00),
(142, 'Cash', '2025-05-10 00:00:00', NULL, 3960.00, 597.00, 1140.00, 60.00, 1797.00, 5757.00, 3960.00, 'pending', '2025-11-10 14:04:29.168367', '2025-11-10 14:04:29.168377', 1, 289, 0.00, 'pending', 3960.00),
(143, 'Cash', '2025-08-28 00:00:00', NULL, 1470.00, 0.00, 0.00, 0.00, 0.00, 1470.00, 1470.00, 'pending', '2025-11-10 14:04:29.248966', '2025-11-10 14:04:29.248976', 1, 218, 0.00, 'pending', 1470.00),
(144, 'Cash', '2024-06-01 00:00:00', NULL, 7000.00, 0.00, 0.00, 0.00, 0.00, 7000.00, 7000.00, 'pending', '2025-11-10 14:04:29.337966', '2025-11-10 14:04:29.337976', 2, 276, 0.00, 'pending', 7000.00),
(145, 'Cash', '2025-02-20 00:00:00', NULL, 1870.00, 220.00, 0.00, 0.00, 220.00, 2090.00, 1870.00, 'pending', '2025-11-10 14:04:29.427440', '2025-11-10 14:04:29.427451', 1, 253, 0.00, 'pending', 1870.00),
(146, 'Cash', '2025-01-09 20:07:00', NULL, 3570.00, 430.00, 0.00, 0.00, 430.00, 4000.00, 3570.00, 'pending', '2025-11-10 14:04:29.504581', '2025-11-10 14:04:29.504591', 4, 273, 0.00, 'pending', 3570.00),
(147, 'Cash', '2025-05-18 00:00:00', NULL, 13600.00, 1650.00, 1200.00, 50.00, 2900.00, 16500.00, 13600.00, 'pending', '2025-11-10 14:04:29.589245', '2025-11-10 14:04:29.589255', 4, 271, 0.00, 'pending', 13600.00),
(148, 'Cash', '2024-07-17 00:00:00', NULL, 4218.00, 0.00, 0.00, 0.00, 0.00, 4218.00, 4218.00, 'pending', '2025-11-10 14:04:29.667591', '2025-11-10 14:04:29.667602', 4, 279, 0.00, 'pending', 4218.00),
(149, 'Cash', '2024-12-14 00:00:00', NULL, 2210.00, 270.00, 0.00, 0.00, 270.00, 2480.00, 2210.00, 'pending', '2025-11-10 14:04:29.806515', '2025-11-10 14:04:29.806525', 1, 231, 0.00, 'pending', 2210.00),
(150, 'Cash', '2024-12-11 00:00:00', NULL, 4030.00, 470.00, 0.00, 0.00, 470.00, 4500.00, 4030.00, 'pending', '2025-11-10 14:04:29.885343', '2025-11-10 14:04:29.885352', 4, 245, 0.00, 'pending', 4030.00),
(151, 'Cash', '2024-06-30 00:00:00', NULL, 2100.00, 0.00, 0.00, 0.00, 0.00, 2100.00, 2100.00, 'pending', '2025-11-10 14:04:29.972770', '2025-11-10 14:04:29.972780', 4, 224, 0.00, 'pending', 2100.00),
(152, 'Cash', '2024-11-24 00:00:00', NULL, 6880.00, 820.00, 0.00, 0.00, 820.00, 7700.00, 6880.00, 'pending', '2025-11-10 14:04:30.058882', '2025-11-10 14:04:30.058892', 4, 252, 0.00, 'pending', 6880.00),
(153, 'Cash', '2025-02-09 00:00:00', NULL, 5090.00, 1510.00, 0.00, 0.00, 1510.00, 6600.00, 5090.00, 'pending', '2025-11-10 14:04:30.144922', '2025-11-10 14:04:30.144932', 1, 233, 0.00, 'pending', 5090.00),
(154, 'Cash', '2025-08-28 00:00:00', NULL, 2140.00, 0.00, 0.00, 2.00, 2.00, 2142.00, 2140.00, 'pending', '2025-11-10 14:04:30.220212', '2025-11-10 14:04:30.220221', 1, 244, 0.00, 'pending', 2140.00),
(155, 'Cash', '2024-07-18 00:00:00', NULL, 2889.00, 0.00, 0.00, 9.00, 9.00, 2898.00, 2889.00, 'pending', '2025-11-10 14:04:30.294566', '2025-11-10 14:04:30.294577', 1, 287, 0.00, 'pending', 2889.00),
(156, 'Cash', '2025-02-07 00:00:00', NULL, 1250.00, 150.00, 0.00, 0.00, 150.00, 1400.00, 1250.00, 'pending', '2025-11-10 14:04:30.366980', '2025-11-10 14:04:30.366990', 1, 272, 0.00, 'pending', 1250.00),
(157, 'Cash', '2024-11-13 00:00:00', NULL, 8610.00, 990.00, 0.00, 0.00, 990.00, 9600.00, 8610.00, 'pending', '2025-11-10 14:04:30.438520', '2025-11-10 14:04:30.438530', 4, 248, 0.00, 'pending', 8610.00),
(158, 'Cash', '2024-12-25 00:00:00', NULL, 5740.00, 2909.00, 0.00, 0.00, 2909.00, 8649.00, 5740.00, 'pending', '2025-11-10 14:04:30.520368', '2025-11-10 14:04:30.520378', 3, 290, 0.00, 'pending', 5740.00),
(159, 'Cash', '2025-06-25 00:00:00', NULL, 1800.00, 350.00, 700.00, 30.00, 1080.00, 2880.00, 1800.00, 'pending', '2025-11-10 14:04:30.597898', '2025-11-10 14:04:30.597908', 1, 263, 0.00, 'pending', 1800.00),
(160, 'Cash', '2024-12-20 00:00:00', NULL, 5619.00, 2386.00, 0.00, 0.00, 2386.00, 8005.00, 5619.00, 'pending', '2025-11-10 14:04:30.675811', '2025-11-10 14:04:30.675821', 3, 234, 0.00, 'pending', 5619.00),
(161, 'Cash', '2024-07-18 00:00:00', NULL, 6640.00, 560.00, 0.00, 0.00, 560.00, 7200.00, 6640.00, 'pending', '2025-11-10 14:04:30.759422', '2025-11-10 14:04:30.759431', 1, 215, 0.00, 'pending', 6640.00),
(162, 'Cash', '2025-06-08 22:57:00', NULL, 5480.00, 770.00, 1400.00, 50.00, 2220.00, 7700.00, 5480.00, 'pending', '2025-11-10 14:04:30.911028', '2025-11-10 14:04:30.911040', 4, 209, 0.00, 'pending', 5480.00),
(163, 'Cash', '2024-06-17 00:00:00', NULL, 3590.00, 90.00, 0.00, 0.00, 90.00, 3680.00, 3590.00, 'pending', '2025-11-10 14:04:30.990855', '2025-11-10 14:04:30.990865', 1, 281, 0.00, 'pending', 3590.00),
(164, 'Cash', '2025-07-11 00:00:00', NULL, 1925.00, 225.00, 0.00, 10.00, 235.00, 2160.00, 1925.00, 'pending', '2025-11-10 14:04:31.069997', '2025-11-10 14:04:31.070007', 1, 286, 0.00, 'pending', 1925.00),
(165, 'Cash', '2025-06-01 00:00:00', NULL, 5799.00, 781.00, 1200.00, 30.00, 2011.00, 7810.00, 5799.00, 'pending', '2025-11-10 14:04:31.227466', '2025-11-10 14:04:31.227476', 4, 236, 0.00, 'pending', 5799.00),
(166, 'Cash', '2025-08-20 00:00:00', NULL, 1105.00, 215.00, 800.00, 30.00, 1045.00, 2150.00, 1105.00, 'pending', '2025-11-10 14:04:31.314444', '2025-11-10 14:04:31.314454', 4, 241, 0.00, 'pending', 1105.00),
(167, 'Cash', '2025-08-03 17:36:00', NULL, 757.00, 173.00, 750.00, 50.00, 973.00, 1730.00, 757.00, 'pending', '2025-11-10 14:04:31.396936', '2025-11-10 14:04:31.396945', 4, 246, 0.00, 'pending', 757.00),
(168, 'Cash', '2025-04-12 09:36:00', NULL, 2840.00, 940.00, 0.00, 0.00, 940.00, 3780.00, 2840.00, 'pending', '2025-11-10 14:04:31.479938', '2025-11-10 14:04:31.479948', 1, 277, 0.00, 'pending', 2840.00),
(169, 'Cash', '2025-02-09 00:00:00', NULL, 6750.00, 0.00, 0.00, 0.00, 0.00, 6750.00, 6750.00, 'pending', '2025-11-10 14:04:31.640671', '2025-11-10 14:04:31.640681', 5, 268, 0.00, 'pending', 6750.00),
(170, 'Cash', '2025-03-09 00:00:00', NULL, 1260.00, 440.00, 0.00, 0.00, 440.00, 1700.00, 1260.00, 'pending', '2025-11-10 14:04:31.717527', '2025-11-10 14:04:31.717537', 4, 242, 0.00, 'pending', 1260.00),
(171, 'Cash', '2025-07-03 00:00:00', NULL, 800.00, 0.00, 0.00, 40.00, 40.00, 840.00, 800.00, 'pending', '2025-11-10 14:04:31.785751', '2025-11-10 14:04:31.785760', 1, 203, 0.00, 'pending', 800.00),
(172, 'Cash', '2025-06-22 00:00:00', NULL, 3450.00, 644.00, 2300.00, 50.00, 2994.00, 6444.00, 3450.00, 'pending', '2025-11-10 14:04:31.861453', '2025-11-10 14:04:31.861462', 3, 238, 0.00, 'pending', 3450.00),
(173, 'Cash', '2024-11-25 00:00:00', NULL, 2330.00, 270.00, 0.00, 0.00, 270.00, 2600.00, 2330.00, 'pending', '2025-11-10 14:04:31.942023', '2025-11-10 14:04:31.942032', 4, 211, 0.00, 'pending', 2330.00),
(174, 'Cash', '2025-01-24 00:00:00', NULL, 3331.00, 2525.00, 0.00, 0.00, 2525.00, 5856.00, 3331.00, 'pending', '2025-11-10 14:04:32.022197', '2025-11-10 14:04:32.022206', 3, 221, 0.00, 'pending', 3331.00),
(175, 'Cash', '2024-12-23 00:00:00', NULL, 3870.00, 2647.00, 0.00, 0.00, 2647.00, 6517.00, 3870.00, 'pending', '2025-11-10 14:04:32.106359', '2025-11-10 14:04:32.106369', 1, 201, 0.00, 'pending', 3870.00);

-- --------------------------------------------------------

--
-- Table structure for table `xe_sale_images`
--

CREATE TABLE `xe_sale_images` (
  `id` bigint(20) NOT NULL,
  `image` varchar(100) NOT NULL,
  `image_name` varchar(255) DEFAULT NULL,
  `description` longtext DEFAULT NULL,
  `is_primary` tinyint(1) NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `sale_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `xe_sale_variants`
--

CREATE TABLE `xe_sale_variants` (
  `id` bigint(20) NOT NULL,
  `quantity` decimal(10,2) NOT NULL,
  `amount_per_unit` decimal(10,2) NOT NULL,
  `total_amount` decimal(12,2) NOT NULL,
  `unit` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `crop_variant_id` bigint(20) NOT NULL,
  `sale_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `xe_sale_variants`
--

INSERT INTO `xe_sale_variants` (`id`, `quantity`, `amount_per_unit`, `total_amount`, `unit`, `created_at`, `crop_variant_id`, `sale_id`) VALUES
(207, 60.00, 164.50, 9870.00, 'Units', '2025-11-10 14:04:25.439018', 10, 97),
(208, 6.00, 165.00, 990.00, 'Units', '2025-11-10 14:04:25.440368', 13, 97),
(209, 2.00, 1300.00, 2600.00, 'Units', '2025-11-10 14:04:25.534775', 5, 98),
(210, 1.00, 500.00, 500.00, 'Units', '2025-11-10 14:04:25.535997', 7, 98),
(211, 1.00, 200.00, 200.00, 'Units', '2025-11-10 14:04:25.536425', 9, 98),
(212, 1.00, 1700.00, 1700.00, 'Units', '2025-11-10 14:04:25.536858', 8, 98),
(213, 23.00, 221.00, 5083.00, 'Units', '2025-11-10 14:04:25.621145', 13, 99),
(214, 3.00, 2267.00, 6801.00, 'Units', '2025-11-10 14:04:25.705777', 5, 100),
(215, 1.00, 800.00, 800.00, 'Units', '2025-11-10 14:04:25.706231', 7, 100),
(216, 1.00, 2700.00, 2700.00, 'Units', '2025-11-10 14:04:25.706656', 8, 100),
(217, 1.00, 800.00, 800.00, 'Units', '2025-11-10 14:04:25.707085', 9, 100),
(218, 252.00, 6.00, 1512.00, 'Units', '2025-11-10 14:04:25.791959', 12, 101),
(219, 46.00, 128.00, 5888.00, 'Units', '2025-11-10 14:04:25.872189', 13, 102),
(220, 1.00, 4000.00, 4000.00, 'Units', '2025-11-10 14:04:25.951934', 5, 103),
(221, 1.00, 4000.00, 4000.00, 'Units', '2025-11-10 14:04:25.952374', 7, 103),
(222, 1.00, 1500.00, 1500.00, 'Units', '2025-11-10 14:04:25.952794', 6, 103),
(223, 1.00, 500.00, 500.00, 'Units', '2025-11-10 14:04:25.953196', 9, 103),
(224, 3.00, 2200.00, 6600.00, 'Units', '2025-11-10 14:04:26.036988', 5, 104),
(225, 2.00, 900.00, 1800.00, 'Units', '2025-11-10 14:04:26.037426', 7, 104),
(226, 2.00, 400.00, 800.00, 'Units', '2025-11-10 14:04:26.037844', 9, 104),
(227, 19.00, 175.00, 3325.00, 'Units', '2025-11-10 14:04:26.115278', 10, 105),
(228, 2.00, 3000.00, 6000.00, 'Units', '2025-11-10 14:04:26.248102', 5, 106),
(229, 2.00, 1850.00, 3700.00, 'Units', '2025-11-10 14:04:26.248528', 7, 106),
(230, 1.00, 900.00, 900.00, 'Units', '2025-11-10 14:04:26.248939', 8, 106),
(231, 2.00, 650.00, 1300.00, 'Units', '2025-11-10 14:04:26.249331', 9, 106),
(232, 15.00, 130.00, 1950.00, 'Units', '2025-11-10 14:04:26.329310', 10, 107),
(233, 2.00, 225.00, 450.00, 'Units', '2025-11-10 14:04:26.329761', 13, 107),
(234, 3.00, 520.00, 1560.00, 'Units', '2025-11-10 14:04:26.410093', 13, 108),
(235, 15.00, 128.00, 1920.00, 'Units', '2025-11-10 14:04:26.410523', 10, 108),
(236, 63.00, 126.00, 7938.00, 'Units', '2025-11-10 14:04:26.486814', 13, 109),
(237, 32.00, 101.00, 3232.00, 'Units', '2025-11-10 14:04:26.571500', 13, 110),
(238, 10.00, 225.00, 2250.00, 'Units', '2025-11-10 14:04:26.643226', 10, 111),
(239, 5.00, 230.00, 1150.00, 'Units', '2025-11-10 14:04:26.643646', 13, 111),
(240, 6.00, 1050.00, 6300.00, 'Units', '2025-11-10 14:04:26.716403', 5, 112),
(241, 2.00, 700.00, 1400.00, 'Units', '2025-11-10 14:04:26.716839', 7, 112),
(242, 1.00, 100.00, 100.00, 'Units', '2025-11-10 14:04:26.717241', 9, 112),
(243, 1.00, 500.00, 500.00, 'Units', '2025-11-10 14:04:26.717644', 8, 112),
(244, 1.00, 300.00, 300.00, 'Units', '2025-11-10 14:04:26.718037', 6, 112),
(245, 23.00, 160.00, 3680.00, 'Units', '2025-11-10 14:04:26.802929', 13, 113),
(246, 50.00, 110.00, 5500.00, 'Units', '2025-11-10 14:04:26.871839', 13, 114),
(247, 54.00, 69.00, 3726.00, 'Units', '2025-11-10 14:04:26.938032', 13, 115),
(248, 40.00, 103.25, 4130.00, 'Units', '2025-11-10 14:04:27.020447', 13, 116),
(249, 18.00, 176.00, 3168.00, 'Units', '2025-11-10 14:04:27.100129', 10, 117),
(250, 2.00, 125.00, 250.00, 'Units', '2025-11-10 14:04:27.100571', 13, 117),
(251, 700.00, 4.00, 2800.00, 'Units', '2025-11-10 14:04:27.173961', 12, 118),
(252, 13.00, 200.00, 2600.00, 'Units', '2025-11-10 14:04:27.307180', 13, 119),
(253, 1.00, 4500.00, 4500.00, 'Units', '2025-11-10 14:04:27.392812', 5, 120),
(254, 1.00, 3500.00, 3500.00, 'Units', '2025-11-10 14:04:27.393226', 7, 120),
(255, 1.00, 1500.00, 1500.00, 'Units', '2025-11-10 14:04:27.393628', 6, 120),
(256, 1.00, 500.00, 500.00, 'Units', '2025-11-10 14:04:27.394018', 9, 120),
(257, 1.00, 800.00, 800.00, 'Units', '2025-11-10 14:04:27.394400', 8, 120),
(258, 12.00, 223.00, 2676.00, 'Units', '2025-11-10 14:04:27.476165', 10, 121),
(259, 3.00, 1177.00, 3531.00, 'Units', '2025-11-10 14:04:27.558846', 5, 122),
(260, 1.00, 616.00, 616.00, 'Units', '2025-11-10 14:04:27.559268', 6, 122),
(261, 1.00, 616.00, 616.00, 'Units', '2025-11-10 14:04:27.559668', 7, 122),
(262, 3.00, 1117.00, 3351.00, 'Units', '2025-11-10 14:04:27.560058', 8, 122),
(263, 2.00, 443.00, 886.00, 'Units', '2025-11-10 14:04:27.560444', 9, 122),
(264, 10.00, 215.00, 2150.00, 'Units', '2025-11-10 14:04:27.639085', 10, 123),
(265, 5.00, 170.00, 850.00, 'Units', '2025-11-10 14:04:27.639508', 13, 123),
(266, 1.00, 2700.00, 2700.00, 'Units', '2025-11-10 14:04:27.713103', 5, 124),
(267, 1.00, 1000.00, 1000.00, 'Units', '2025-11-10 14:04:27.713541', 6, 124),
(268, 1.00, 300.00, 300.00, 'Units', '2025-11-10 14:04:27.713951', 7, 124),
(269, 2.00, 175.00, 350.00, 'Units', '2025-11-10 14:04:27.714348', 9, 124),
(270, 2.00, 1200.00, 2400.00, 'Units', '2025-11-10 14:04:27.714750', 8, 124),
(271, 24.00, 132.00, 3168.00, 'Units', '2025-11-10 14:04:27.789707', 13, 125),
(272, 1.00, 800.00, 800.00, 'Units', '2025-11-10 14:04:27.863373', 5, 126),
(273, 1.00, 500.00, 500.00, 'Units', '2025-11-10 14:04:27.863794', 7, 126),
(274, 1.00, 350.00, 350.00, 'Units', '2025-11-10 14:04:27.864190', 8, 126),
(275, 1.00, 100.00, 100.00, 'Units', '2025-11-10 14:04:27.864579', 9, 126),
(276, 1.00, 700.00, 700.00, 'Units', '2025-11-10 14:04:27.941499', 5, 127),
(277, 1.00, 50.00, 50.00, 'Units', '2025-11-10 14:04:27.941943', 9, 127),
(278, 1.00, 400.00, 400.00, 'Units', '2025-11-10 14:04:27.942345', 8, 127),
(279, 4.00, 1788.00, 7152.00, 'Units', '2025-11-10 14:04:28.032511', 5, 128),
(280, 1.00, 1920.00, 1920.00, 'Units', '2025-11-10 14:04:28.032946', 7, 128),
(281, 1.00, 1920.00, 1920.00, 'Units', '2025-11-10 14:04:28.033345', 6, 128),
(282, 3.00, 842.00, 2526.00, 'Units', '2025-11-10 14:04:28.033748', 9, 128),
(283, 1.00, 1800.00, 1800.00, 'Units', '2025-11-10 14:04:28.034144', 8, 128),
(284, 2.00, 1400.00, 2800.00, 'Units', '2025-11-10 14:04:28.127521', 5, 129),
(285, 1.00, 500.00, 500.00, 'Units', '2025-11-10 14:04:28.127959', 7, 129),
(286, 1.00, 100.00, 100.00, 'Units', '2025-11-10 14:04:28.128361', 9, 129),
(287, 6.00, 1288.00, 7728.00, 'Units', '2025-11-10 14:04:28.209509', 5, 130),
(288, 2.00, 785.00, 1570.00, 'Units', '2025-11-10 14:04:28.209937', 7, 130),
(289, 3.00, 570.00, 1710.00, 'Units', '2025-11-10 14:04:28.210333', 9, 130),
(290, 8.00, 168.75, 1350.00, 'Units', '2025-11-10 14:04:28.288991', 13, 131),
(291, 8.00, 225.00, 1800.00, 'Units', '2025-11-10 14:04:28.289407', 10, 131),
(292, 2.00, 325.00, 650.00, 'Units', '2025-11-10 14:04:28.371449', 13, 132),
(293, 10.00, 168.00, 1680.00, 'Units', '2025-11-10 14:04:28.449978', 13, 133),
(294, 12.00, 156.00, 1872.00, 'Units', '2025-11-10 14:04:28.526742', 10, 134),
(295, 3.00, 156.00, 468.00, 'Units', '2025-11-10 14:04:28.527209', 13, 134),
(296, 2.00, 700.00, 1400.00, 'Units', '2025-11-10 14:04:28.603181', 5, 135),
(297, 2.00, 200.00, 400.00, 'Units', '2025-11-10 14:04:28.603623', 7, 135),
(298, 4.00, 1450.00, 5800.00, 'Units', '2025-11-10 14:04:28.604027', 8, 135),
(299, 3.00, 100.00, 300.00, 'Units', '2025-11-10 14:04:28.604419', 9, 135),
(300, 3.00, 2000.00, 6000.00, 'Units', '2025-11-10 14:04:28.682922', 5, 136),
(301, 2.00, 1000.00, 2000.00, 'Units', '2025-11-10 14:04:28.683357', 7, 136),
(302, 1.00, 300.00, 300.00, 'Units', '2025-11-10 14:04:28.683773', 9, 136),
(303, 1.00, 300.00, 300.00, 'Units', '2025-11-10 14:04:28.684177', 8, 136),
(304, 59.00, 91.00, 5369.00, 'Units', '2025-11-10 14:04:28.756118', 13, 137),
(305, 2.00, 2000.00, 4000.00, 'Units', '2025-11-10 14:04:28.829525', 5, 138),
(306, 1.00, 2300.00, 2300.00, 'Units', '2025-11-10 14:04:28.829973', 8, 138),
(307, 1.00, 1600.00, 1600.00, 'Units', '2025-11-10 14:04:28.830384', 7, 138),
(308, 2.00, 750.00, 1500.00, 'Units', '2025-11-10 14:04:28.830789', 9, 138),
(309, 10.00, 205.00, 2050.00, 'Units', '2025-11-10 14:04:28.909433', 10, 139),
(310, 3.00, 1420.00, 4260.00, 'Units', '2025-11-10 14:04:28.990963', 5, 140),
(311, 2.00, 614.00, 1228.00, 'Units', '2025-11-10 14:04:28.991412', 9, 140),
(312, 1.00, 1050.00, 1050.00, 'Units', '2025-11-10 14:04:28.991827', 7, 140),
(313, 9.00, 1471.00, 13239.00, 'Units', '2025-11-10 14:04:28.992221', 8, 140),
(314, 1.00, 3800.00, 3800.00, 'Units', '2025-11-10 14:04:29.078678', 5, 141),
(315, 1.00, 2500.00, 2500.00, 'Units', '2025-11-10 14:04:29.079115', 7, 141),
(316, 1.00, 2000.00, 2000.00, 'Units', '2025-11-10 14:04:29.079521', 6, 141),
(317, 1.00, 400.00, 400.00, 'Units', '2025-11-10 14:04:29.079930', 9, 141),
(318, 1.00, 1000.00, 1000.00, 'Units', '2025-11-10 14:04:29.080328', 8, 141),
(319, 57.00, 101.00, 5757.00, 'Units', '2025-11-10 14:04:29.169110', 13, 142),
(320, 1.00, 147.00, 147.00, 'Units', '2025-11-10 14:04:29.249594', 13, 143),
(321, 9.00, 147.00, 1323.00, 'Units', '2025-11-10 14:04:29.250016', 10, 143),
(322, 1.00, 7000.00, 7000.00, 'Units', '2025-11-10 14:04:29.338477', 18, 144),
(323, 11.00, 190.00, 2090.00, 'Units', '2025-11-10 14:04:29.428349', 10, 145),
(324, 4.00, 725.00, 2900.00, 'Units', '2025-11-10 14:04:29.505179', 5, 146),
(325, 2.00, 400.00, 800.00, 'Units', '2025-11-10 14:04:29.505625', 7, 146),
(326, 2.00, 150.00, 300.00, 'Units', '2025-11-10 14:04:29.506028', 9, 146),
(327, 2.00, 4000.00, 8000.00, 'Units', '2025-11-10 14:04:29.589933', 5, 147),
(328, 1.00, 3000.00, 3000.00, 'Units', '2025-11-10 14:04:29.590359', 7, 147),
(329, 2.00, 2000.00, 4000.00, 'Units', '2025-11-10 14:04:29.590771', 6, 147),
(330, 1.00, 500.00, 500.00, 'Units', '2025-11-10 14:04:29.591167', 9, 147),
(331, 1.00, 1000.00, 1000.00, 'Units', '2025-11-10 14:04:29.591566', 8, 147),
(332, 3.00, 1406.00, 4218.00, 'Units', '2025-11-10 14:04:29.668182', 7, 148),
(333, 16.00, 155.00, 2480.00, 'Units', '2025-11-10 14:04:29.808192', 10, 149),
(334, 3.00, 1000.00, 3000.00, 'Units', '2025-11-10 14:04:29.886970', 5, 150),
(335, 1.00, 500.00, 500.00, 'Units', '2025-11-10 14:04:29.887400', 7, 150),
(336, 2.00, 500.00, 1000.00, 'Units', '2025-11-10 14:04:29.887808', 9, 150),
(337, 3.00, 700.00, 2100.00, 'Units', '2025-11-10 14:04:29.974315', 7, 151),
(338, 5.00, 1300.00, 6500.00, 'Units', '2025-11-10 14:04:30.059581', 5, 152),
(339, 1.00, 900.00, 900.00, 'Units', '2025-11-10 14:04:30.060011', 7, 152),
(340, 1.00, 300.00, 300.00, 'Units', '2025-11-10 14:04:30.060414', 9, 152),
(341, 1.00, 1000.00, 1000.00, 'Units', '2025-11-10 14:04:30.146120', 5, 153),
(342, 2.00, 200.00, 400.00, 'Units', '2025-11-10 14:04:30.146551', 7, 153),
(343, 2.00, 2500.00, 5000.00, 'Units', '2025-11-10 14:04:30.146955', 8, 153),
(344, 2.00, 100.00, 200.00, 'Units', '2025-11-10 14:04:30.147344', 9, 153),
(345, 17.00, 126.00, 2142.00, 'Units', '2025-11-10 14:04:30.221249', 13, 154),
(346, 14.00, 207.00, 2898.00, 'Units', '2025-11-10 14:04:30.295543', 13, 155),
(347, 10.00, 140.00, 1400.00, 'Units', '2025-11-10 14:04:30.367841', 13, 156),
(348, 4.00, 1500.00, 6000.00, 'Units', '2025-11-10 14:04:30.439333', 5, 157),
(349, 2.00, 1400.00, 2800.00, 'Units', '2025-11-10 14:04:30.439779', 7, 157),
(350, 2.00, 300.00, 600.00, 'Units', '2025-11-10 14:04:30.440185', 8, 157),
(351, 2.00, 100.00, 200.00, 'Units', '2025-11-10 14:04:30.440587', 9, 157),
(352, 4.00, 1365.00, 5460.00, 'Units', '2025-11-10 14:04:30.521147', 5, 158),
(353, 2.00, 643.50, 1287.00, 'Units', '2025-11-10 14:04:30.521583', 7, 158),
(354, 3.00, 634.00, 1902.00, 'Units', '2025-11-10 14:04:30.521983', 9, 158),
(355, 30.00, 96.00, 2880.00, 'Units', '2025-11-10 14:04:30.598905', 13, 159),
(356, 4.00, 1440.00, 5760.00, 'Units', '2025-11-10 14:04:30.676594', 5, 160),
(357, 1.00, 925.00, 925.00, 'Units', '2025-11-10 14:04:30.677027', 7, 160),
(358, 2.00, 660.00, 1320.00, 'Units', '2025-11-10 14:04:30.677428', 9, 160),
(359, 80.00, 90.00, 7200.00, 'Units', '2025-11-10 14:04:30.760566', 13, 161),
(360, 1.00, 1700.00, 1700.00, 'Units', '2025-11-10 14:04:30.911963', 5, 162),
(361, 3.00, 200.00, 600.00, 'Units', '2025-11-10 14:04:30.912418', 8, 162),
(362, 2.00, 2000.00, 4000.00, 'Units', '2025-11-10 14:04:30.912858', 7, 162),
(363, 1.00, 700.00, 700.00, 'Units', '2025-11-10 14:04:30.913272', 6, 162),
(364, 2.00, 350.00, 700.00, 'Units', '2025-11-10 14:04:30.913677', 9, 162),
(365, 23.00, 160.00, 3680.00, 'Units', '2025-11-10 14:04:30.991614', 13, 163),
(366, 8.00, 270.00, 2160.00, 'Units', '2025-11-10 14:04:31.071529', 13, 164),
(367, 2.00, 2000.00, 4000.00, 'Units', '2025-11-10 14:04:31.228153', 5, 165),
(368, 1.00, 1500.00, 1500.00, 'Units', '2025-11-10 14:04:31.228581', 7, 165),
(369, 2.00, 550.00, 1100.00, 'Units', '2025-11-10 14:04:31.228984', 9, 165),
(370, 1.00, 1200.00, 1200.00, 'Units', '2025-11-10 14:04:31.229373', 6, 165),
(371, 1.00, 10.00, 10.00, 'Units', '2025-11-10 14:04:31.229772', 8, 165),
(372, 1.00, 1000.00, 1000.00, 'Units', '2025-11-10 14:04:31.315027', 5, 166),
(373, 2.00, 550.00, 1100.00, 'Units', '2025-11-10 14:04:31.315453', 7, 166),
(374, 1.00, 50.00, 50.00, 'Units', '2025-11-10 14:04:31.315866', 9, 166),
(375, 1.00, 800.00, 800.00, 'Units', '2025-11-10 14:04:31.397467', 5, 167),
(376, 1.00, 300.00, 300.00, 'Units', '2025-11-10 14:04:31.397900', 7, 167),
(377, 2.00, 65.00, 130.00, 'Units', '2025-11-10 14:04:31.398301', 9, 167),
(378, 1.00, 400.00, 400.00, 'Units', '2025-11-10 14:04:31.398708', 8, 167),
(379, 1.00, 100.00, 100.00, 'Units', '2025-11-10 14:04:31.399101', 6, 167),
(380, 17.00, 180.00, 3060.00, 'Units', '2025-11-10 14:04:31.480885', 10, 168),
(381, 4.00, 180.00, 720.00, 'Units', '2025-11-10 14:04:31.481300', 13, 168),
(382, 3.00, 2250.00, 6750.00, 'Units', '2025-11-10 14:04:31.641196', 16, 169),
(383, 2.00, 850.00, 1700.00, 'Units', '2025-11-10 14:04:31.718092', 8, 170),
(384, 120.00, 7.00, 840.00, 'Units', '2025-11-10 14:04:31.786257', 12, 171),
(385, 1.00, 860.00, 860.00, 'Units', '2025-11-10 14:04:31.862011', 5, 172),
(386, 4.00, 1245.00, 4980.00, 'Units', '2025-11-10 14:04:31.862430', 8, 172),
(387, 2.00, 236.00, 472.00, 'Units', '2025-11-10 14:04:31.862835', 7, 172),
(388, 3.00, 44.00, 132.00, 'Units', '2025-11-10 14:04:31.863225', 9, 172),
(389, 400.00, 6.50, 2600.00, 'Units', '2025-11-10 14:04:31.942758', 12, 173),
(390, 3.00, 890.00, 2670.00, 'Units', '2025-11-10 14:04:32.022718', 5, 174),
(391, 1.00, 782.00, 782.00, 'Units', '2025-11-10 14:04:32.023134', 7, 174),
(392, 1.00, 544.00, 544.00, 'Units', '2025-11-10 14:04:32.023525', 6, 174),
(393, 3.00, 620.00, 1860.00, 'Units', '2025-11-10 14:04:32.023926', 9, 174),
(394, 44.00, 133.00, 5852.00, 'Units', '2025-11-10 14:04:32.107601', 10, 175),
(395, 5.00, 133.00, 665.00, 'Units', '2025-11-10 14:04:32.108017', 13, 175);

-- --------------------------------------------------------

--
-- Table structure for table `xe_wages`
--

CREATE TABLE `xe_wages` (
  `id` bigint(20) NOT NULL,
  `effective_from` date NOT NULL,
  `effective_to` date DEFAULT NULL,
  `amount` decimal(10,2) NOT NULL,
  `remarks` longtext DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `employee_id` bigint(20) NOT NULL
) ;

--
-- Dumping data for table `xe_wages`
--

INSERT INTO `xe_wages` (`id`, `effective_from`, `effective_to`, `amount`, `remarks`, `created_at`, `updated_at`, `employee_id`) VALUES
(35, '2024-07-01', '2027-12-31', 500.00, '', '2025-11-07 10:55:06.520585', '2025-11-07 10:55:06.520617', 31),
(36, '2024-07-01', '2027-12-31', 500.00, '', '2025-11-07 10:55:06.525094', '2025-11-07 10:55:06.525116', 33),
(37, '2024-07-01', '2027-12-31', 500.00, '', '2025-11-07 10:55:06.529658', '2025-11-07 10:55:06.529673', 35),
(38, '2024-07-01', '2027-12-31', 500.00, '', '2025-11-07 10:55:06.533822', '2025-11-07 10:55:06.533837', 36),
(39, '2024-07-01', '2027-12-31', 500.00, '', '2025-11-07 10:55:06.537887', '2025-11-07 10:55:06.537901', 37),
(40, '2024-07-01', '2027-12-31', 500.00, '', '2025-11-07 10:55:06.542059', '2025-11-07 10:55:06.542073', 40),
(41, '2024-07-01', '2027-12-31', 500.00, '', '2025-11-07 10:55:06.546158', '2025-11-07 10:55:06.546172', 44),
(42, '2024-07-01', '2027-12-31', 500.00, '', '2025-11-07 10:55:06.550179', '2025-11-07 10:55:06.550193', 46),
(43, '2024-07-01', '2027-12-31', 500.00, '', '2025-11-07 10:55:06.554639', '2025-11-07 10:55:06.554653', 50),
(44, '2024-07-01', '2027-12-31', 500.00, '', '2025-11-07 10:55:06.558774', '2025-11-07 10:55:06.558787', 51),
(45, '2024-07-01', '2027-12-31', 500.00, '', '2025-11-07 10:55:06.562790', '2025-11-07 10:55:06.562804', 52),
(46, '2024-07-01', '2027-12-31', 500.00, '', '2025-11-07 10:55:06.566776', '2025-11-07 10:55:06.566790', 53),
(47, '2024-07-01', '2027-12-31', 500.00, '', '2025-11-07 10:55:06.570756', '2025-11-07 10:55:06.570769', 54),
(48, '2024-07-01', '2027-12-31', 500.00, '', '2025-11-07 10:55:06.574684', '2025-11-07 10:55:06.574698', 55),
(49, '2024-06-01', '2026-12-31', 200.00, '', '2025-11-07 10:55:38.879585', '2025-11-07 10:55:38.879603', 32),
(50, '2024-05-01', '2026-12-31', 300.00, '', '2025-11-07 10:56:26.184251', '2025-11-07 10:56:26.184282', 34),
(51, '2024-05-01', '2026-12-31', 300.00, '', '2025-11-07 10:56:26.188768', '2025-11-07 10:56:26.188783', 38),
(52, '2024-05-01', '2026-12-31', 300.00, '', '2025-11-07 10:56:26.192918', '2025-11-07 10:56:26.192933', 39),
(53, '2024-05-01', '2026-12-31', 300.00, '', '2025-11-07 10:56:26.197085', '2025-11-07 10:56:26.197099', 41),
(54, '2024-05-01', '2026-12-31', 300.00, '', '2025-11-07 10:56:26.201136', '2025-11-07 10:56:26.201150', 42),
(55, '2024-05-01', '2026-12-31', 300.00, '', '2025-11-07 10:56:26.205725', '2025-11-07 10:56:26.205739', 48),
(56, '2024-05-01', '2026-12-31', 450.00, NULL, '2025-11-07 10:57:22.821098', '2025-11-07 11:51:52.204908', 43),
(57, '2024-04-01', '2026-12-31', 450.00, NULL, '2025-11-07 10:57:22.825334', '2025-11-07 11:47:16.725192', 47),
(58, '2024-05-01', '2026-12-31', 450.00, NULL, '2025-11-07 10:57:22.829336', '2025-11-07 11:52:14.739998', 49);

-- --------------------------------------------------------

--
-- Table structure for table `xe_wage_payment_transactions`
--

CREATE TABLE `xe_wage_payment_transactions` (
  `id` bigint(20) NOT NULL,
  `transaction_type` varchar(20) NOT NULL,
  `amount` decimal(12,2) NOT NULL,
  `payment_mode` varchar(20) NOT NULL,
  `reference_number` varchar(255) DEFAULT NULL,
  `transaction_date` datetime(6) NOT NULL,
  `remarks` longtext DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `wage_payment_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `xe_weekly_wage_payment`
--

CREATE TABLE `xe_weekly_wage_payment` (
  `id` bigint(20) NOT NULL,
  `week_start_date` date NOT NULL,
  `week_end_date` date NOT NULL,
  `total_deductions` decimal(15,2) NOT NULL,
  `payment_status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `expense_entry_id` bigint(20) DEFAULT NULL,
  `employee_wages` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`employee_wages`)),
  `total_employees` int(10) UNSIGNED NOT NULL CHECK (`total_employees` >= 0),
  `total_gross_amount` decimal(15,2) NOT NULL,
  `total_net_amount` decimal(15,2) NOT NULL,
  `total_paid_amount` decimal(15,2) NOT NULL,
  `total_remaining_amount` decimal(15,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `xe_weekly_wage_payment`
--

INSERT INTO `xe_weekly_wage_payment` (`id`, `week_start_date`, `week_end_date`, `total_deductions`, `payment_status`, `created_at`, `updated_at`, `expense_entry_id`, `employee_wages`, `total_employees`, `total_gross_amount`, `total_net_amount`, `total_paid_amount`, `total_remaining_amount`) VALUES
(35, '2025-11-03', '2025-11-09', 0.00, 'paid', '2025-11-12 06:23:38.953810', '2025-11-12 06:23:38.957292', 686, '[{\"employee_id\": \"31\", \"employee_name\": \"Pitchai\", \"present_days\": 5, \"half_days\": 0, \"late_days\": 0, \"daily_wage\": 500.0, \"gross_amount\": 2500.0, \"advance_deduction\": 0.0, \"other_deductions\": 0.0, \"total_deductions\": 0.0, \"net_amount\": 2500.0, \"paid_amount\": 2500.0, \"remaining_amount\": 0.0, \"payment_status\": \"paid\", \"payment_mode\": \"Cash\", \"payment_date\": \"2025-11-12T06:23:38.956160+00:00\", \"payment_reference\": \"\", \"remarks\": \"Bulk wage payment for week 2025-11-03\", \"attendance_details\": {\"2025-11-03\": {\"status\": 1, \"wage_rate\": 500.0, \"wage_earned\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, \"2025-11-04\": {\"status\": 1, \"wage_rate\": 500.0, \"wage_earned\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, \"2025-11-05\": {\"status\": 1, \"wage_rate\": 500.0, \"wage_earned\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, \"2025-11-06\": {\"status\": 1, \"wage_rate\": 500.0, \"wage_earned\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, \"2025-11-07\": {\"status\": 1, \"wage_rate\": 500.0, \"wage_earned\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, \"2025-11-08\": {\"status\": null, \"wage_rate\": 500.0, \"wage_earned\": 0.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, \"2025-11-09\": {\"status\": null, \"wage_rate\": 500.0, \"wage_earned\": 0.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}}, \"last_payment_date\": null, \"payment_remarks\": \"\", \"historical_wage_calculation\": {\"enabled\": true, \"primary_wage_rate\": 500.0, \"effective_from\": \"2024-07-01\", \"effective_to\": \"2027-12-31\", \"daily_rates_used\": [500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0], \"multiple_rates_in_week\": false, \"calculation_date\": \"2025-11-03\"}}, {\"employee_id\": \"32\", \"employee_name\": \"Chinnammal\", \"present_days\": 5, \"half_days\": 0, \"late_days\": 0, \"daily_wage\": 200.0, \"gross_amount\": 1000.0, \"advance_deduction\": 0.0, \"other_deductions\": 0.0, \"total_deductions\": 0.0, \"net_amount\": 1000.0, \"paid_amount\": 1000.0, \"remaining_amount\": 0.0, \"payment_status\": \"paid\", \"payment_mode\": \"Cash\", \"payment_date\": \"2025-11-12T06:23:38.956173+00:00\", \"payment_reference\": \"\", \"remarks\": \"Bulk wage payment for week 2025-11-03\", \"attendance_details\": {\"2025-11-03\": {\"status\": 1, \"wage_rate\": 200.0, \"wage_earned\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, \"2025-11-04\": {\"status\": 1, \"wage_rate\": 200.0, \"wage_earned\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, \"2025-11-05\": {\"status\": 1, \"wage_rate\": 200.0, \"wage_earned\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, \"2025-11-06\": {\"status\": 1, \"wage_rate\": 200.0, \"wage_earned\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, \"2025-11-07\": {\"status\": 1, \"wage_rate\": 200.0, \"wage_earned\": 200.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, \"2025-11-08\": {\"status\": null, \"wage_rate\": 200.0, \"wage_earned\": 0.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}, \"2025-11-09\": {\"status\": null, \"wage_rate\": 200.0, \"wage_earned\": 0.0, \"wage_effective_from\": \"2024-06-01\", \"wage_effective_to\": \"2026-12-31\"}}, \"last_payment_date\": null, \"payment_remarks\": \"\", \"historical_wage_calculation\": {\"enabled\": true, \"primary_wage_rate\": 200.0, \"effective_from\": \"2024-06-01\", \"effective_to\": \"2026-12-31\", \"daily_rates_used\": [200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0], \"multiple_rates_in_week\": false, \"calculation_date\": \"2025-11-03\"}}, {\"employee_id\": \"54\", \"employee_name\": \"Iyappan\", \"present_days\": 4, \"half_days\": 0, \"late_days\": 0, \"daily_wage\": 500.0, \"gross_amount\": 2000.0, \"advance_deduction\": 0.0, \"other_deductions\": 0.0, \"total_deductions\": 0.0, \"net_amount\": 2000.0, \"paid_amount\": 2000.0, \"remaining_amount\": 0.0, \"payment_status\": \"paid\", \"payment_mode\": \"Cash\", \"payment_date\": \"2025-11-12T06:23:38.956179+00:00\", \"payment_reference\": \"\", \"remarks\": \"Bulk wage payment for week 2025-11-03\", \"attendance_details\": {\"2025-11-03\": {\"status\": 1, \"wage_rate\": 500.0, \"wage_earned\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, \"2025-11-04\": {\"status\": 1, \"wage_rate\": 500.0, \"wage_earned\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, \"2025-11-05\": {\"status\": null, \"wage_rate\": 500.0, \"wage_earned\": 0.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, \"2025-11-06\": {\"status\": 1, \"wage_rate\": 500.0, \"wage_earned\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, \"2025-11-07\": {\"status\": 1, \"wage_rate\": 500.0, \"wage_earned\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, \"2025-11-08\": {\"status\": null, \"wage_rate\": 500.0, \"wage_earned\": 0.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, \"2025-11-09\": {\"status\": null, \"wage_rate\": 500.0, \"wage_earned\": 0.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}}, \"last_payment_date\": null, \"payment_remarks\": \"\", \"historical_wage_calculation\": {\"enabled\": true, \"primary_wage_rate\": 500.0, \"effective_from\": \"2024-07-01\", \"effective_to\": \"2027-12-31\", \"daily_rates_used\": [500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0], \"multiple_rates_in_week\": false, \"calculation_date\": \"2025-11-03\"}}, {\"employee_id\": \"41\", \"employee_name\": \"Banu\", \"present_days\": 2, \"half_days\": 0, \"late_days\": 0, \"daily_wage\": 300.0, \"gross_amount\": 600.0, \"advance_deduction\": 0.0, \"other_deductions\": 0.0, \"total_deductions\": 0.0, \"net_amount\": 600.0, \"paid_amount\": 600.0, \"remaining_amount\": 0.0, \"payment_status\": \"paid\", \"payment_mode\": \"Cash\", \"payment_date\": \"2025-11-12T06:23:38.956183+00:00\", \"payment_reference\": \"\", \"remarks\": \"Bulk wage payment for week 2025-11-03\", \"attendance_details\": {\"2025-11-03\": {\"status\": null, \"wage_rate\": 300.0, \"wage_earned\": 0.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, \"2025-11-04\": {\"status\": 1, \"wage_rate\": 300.0, \"wage_earned\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, \"2025-11-05\": {\"status\": null, \"wage_rate\": 300.0, \"wage_earned\": 0.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, \"2025-11-06\": {\"status\": null, \"wage_rate\": 300.0, \"wage_earned\": 0.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, \"2025-11-07\": {\"status\": 1, \"wage_rate\": 300.0, \"wage_earned\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, \"2025-11-08\": {\"status\": null, \"wage_rate\": 300.0, \"wage_earned\": 0.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, \"2025-11-09\": {\"status\": null, \"wage_rate\": 300.0, \"wage_earned\": 0.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}}, \"last_payment_date\": null, \"payment_remarks\": \"\", \"historical_wage_calculation\": {\"enabled\": true, \"primary_wage_rate\": 300.0, \"effective_from\": \"2024-05-01\", \"effective_to\": \"2026-12-31\", \"daily_rates_used\": [300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0], \"multiple_rates_in_week\": false, \"calculation_date\": \"2025-11-03\"}}, {\"employee_id\": \"53\", \"employee_name\": \"Nagesh\", \"present_days\": 5, \"half_days\": 0, \"late_days\": 0, \"daily_wage\": 500.0, \"gross_amount\": 2500.0, \"advance_deduction\": 0.0, \"other_deductions\": 0.0, \"total_deductions\": 0.0, \"net_amount\": 2500.0, \"paid_amount\": 2500.0, \"remaining_amount\": 0.0, \"payment_status\": \"paid\", \"payment_mode\": \"Cash\", \"payment_date\": \"2025-11-12T06:23:38.956187+00:00\", \"payment_reference\": \"\", \"remarks\": \"Bulk wage payment for week 2025-11-03\", \"attendance_details\": {\"2025-11-03\": {\"status\": 1, \"wage_rate\": 500.0, \"wage_earned\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, \"2025-11-04\": {\"status\": 1, \"wage_rate\": 500.0, \"wage_earned\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, \"2025-11-05\": {\"status\": 1, \"wage_rate\": 500.0, \"wage_earned\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, \"2025-11-06\": {\"status\": 1, \"wage_rate\": 500.0, \"wage_earned\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, \"2025-11-07\": {\"status\": 1, \"wage_rate\": 500.0, \"wage_earned\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, \"2025-11-08\": {\"status\": null, \"wage_rate\": 500.0, \"wage_earned\": 0.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, \"2025-11-09\": {\"status\": null, \"wage_rate\": 500.0, \"wage_earned\": 0.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}}, \"last_payment_date\": null, \"payment_remarks\": \"\", \"historical_wage_calculation\": {\"enabled\": true, \"primary_wage_rate\": 500.0, \"effective_from\": \"2024-07-01\", \"effective_to\": \"2027-12-31\", \"daily_rates_used\": [500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0], \"multiple_rates_in_week\": false, \"calculation_date\": \"2025-11-03\"}}, {\"employee_id\": \"43\", \"employee_name\": \"Elliajar Tete\", \"present_days\": 4, \"half_days\": 0, \"late_days\": 0, \"daily_wage\": 450.0, \"gross_amount\": 1800.0, \"advance_deduction\": 0.0, \"other_deductions\": 0.0, \"total_deductions\": 0.0, \"net_amount\": 1800.0, \"paid_amount\": 1800.0, \"remaining_amount\": 0.0, \"payment_status\": \"paid\", \"payment_mode\": \"Cash\", \"payment_date\": \"2025-11-12T06:23:38.956191+00:00\", \"payment_reference\": \"\", \"remarks\": \"Bulk wage payment for week 2025-11-03\", \"attendance_details\": {\"2025-11-03\": {\"status\": 1, \"wage_rate\": 450.0, \"wage_earned\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, \"2025-11-04\": {\"status\": 1, \"wage_rate\": 450.0, \"wage_earned\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, \"2025-11-05\": {\"status\": null, \"wage_rate\": 450.0, \"wage_earned\": 0.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, \"2025-11-06\": {\"status\": 1, \"wage_rate\": 450.0, \"wage_earned\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, \"2025-11-07\": {\"status\": 1, \"wage_rate\": 450.0, \"wage_earned\": 450.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, \"2025-11-08\": {\"status\": null, \"wage_rate\": 450.0, \"wage_earned\": 0.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, \"2025-11-09\": {\"status\": null, \"wage_rate\": 450.0, \"wage_earned\": 0.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}}, \"last_payment_date\": null, \"payment_remarks\": \"\", \"historical_wage_calculation\": {\"enabled\": true, \"primary_wage_rate\": 450.0, \"effective_from\": \"2024-05-01\", \"effective_to\": \"2026-12-31\", \"daily_rates_used\": [450.0, 450.0, 450.0, 450.0, 450.0, 450.0, 450.0], \"multiple_rates_in_week\": false, \"calculation_date\": \"2025-11-03\"}}, {\"employee_id\": \"34\", \"employee_name\": \"Rebeka\", \"present_days\": 4, \"half_days\": 0, \"late_days\": 0, \"daily_wage\": 300.0, \"gross_amount\": 1200.0, \"advance_deduction\": 0.0, \"other_deductions\": 0.0, \"total_deductions\": 0.0, \"net_amount\": 1200.0, \"paid_amount\": 1200.0, \"remaining_amount\": 0.0, \"payment_status\": \"paid\", \"payment_mode\": \"Cash\", \"payment_date\": \"2025-11-12T06:23:38.956194+00:00\", \"payment_reference\": \"\", \"remarks\": \"Bulk wage payment for week 2025-11-03\", \"attendance_details\": {\"2025-11-03\": {\"status\": 1, \"wage_rate\": 300.0, \"wage_earned\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, \"2025-11-04\": {\"status\": 1, \"wage_rate\": 300.0, \"wage_earned\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, \"2025-11-05\": {\"status\": null, \"wage_rate\": 300.0, \"wage_earned\": 0.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, \"2025-11-06\": {\"status\": 1, \"wage_rate\": 300.0, \"wage_earned\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, \"2025-11-07\": {\"status\": 1, \"wage_rate\": 300.0, \"wage_earned\": 300.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, \"2025-11-08\": {\"status\": null, \"wage_rate\": 300.0, \"wage_earned\": 0.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}, \"2025-11-09\": {\"status\": null, \"wage_rate\": 300.0, \"wage_earned\": 0.0, \"wage_effective_from\": \"2024-05-01\", \"wage_effective_to\": \"2026-12-31\"}}, \"last_payment_date\": null, \"payment_remarks\": \"\", \"historical_wage_calculation\": {\"enabled\": true, \"primary_wage_rate\": 300.0, \"effective_from\": \"2024-05-01\", \"effective_to\": \"2026-12-31\", \"daily_rates_used\": [300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0], \"multiple_rates_in_week\": false, \"calculation_date\": \"2025-11-03\"}}, {\"employee_id\": \"36\", \"employee_name\": \"Thirumurugan\", \"present_days\": 2, \"half_days\": 0, \"late_days\": 0, \"daily_wage\": 500.0, \"gross_amount\": 1000.0, \"advance_deduction\": 0.0, \"other_deductions\": 0.0, \"total_deductions\": 0.0, \"net_amount\": 1000.0, \"paid_amount\": 1000.0, \"remaining_amount\": 0.0, \"payment_status\": \"paid\", \"payment_mode\": \"Cash\", \"payment_date\": \"2025-11-12T06:23:38.956198+00:00\", \"payment_reference\": \"\", \"remarks\": \"Bulk wage payment for week 2025-11-03\", \"attendance_details\": {\"2025-11-03\": {\"status\": null, \"wage_rate\": 500.0, \"wage_earned\": 0.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, \"2025-11-04\": {\"status\": null, \"wage_rate\": 500.0, \"wage_earned\": 0.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, \"2025-11-05\": {\"status\": null, \"wage_rate\": 500.0, \"wage_earned\": 0.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, \"2025-11-06\": {\"status\": 1, \"wage_rate\": 500.0, \"wage_earned\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, \"2025-11-07\": {\"status\": 1, \"wage_rate\": 500.0, \"wage_earned\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, \"2025-11-08\": {\"status\": null, \"wage_rate\": 500.0, \"wage_earned\": 0.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, \"2025-11-09\": {\"status\": null, \"wage_rate\": 500.0, \"wage_earned\": 0.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}}, \"last_payment_date\": null, \"payment_remarks\": \"\", \"historical_wage_calculation\": {\"enabled\": true, \"primary_wage_rate\": 500.0, \"effective_from\": \"2024-07-01\", \"effective_to\": \"2027-12-31\", \"daily_rates_used\": [500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0], \"multiple_rates_in_week\": false, \"calculation_date\": \"2025-11-03\"}}, {\"employee_id\": \"37\", \"employee_name\": \"Mohan\", \"present_days\": 2, \"half_days\": 0, \"late_days\": 0, \"daily_wage\": 500.0, \"gross_amount\": 1000.0, \"advance_deduction\": 0.0, \"other_deductions\": 0.0, \"total_deductions\": 0.0, \"net_amount\": 1000.0, \"paid_amount\": 1000.0, \"remaining_amount\": 0.0, \"payment_status\": \"paid\", \"payment_mode\": \"Cash\", \"payment_date\": \"2025-11-12T06:23:38.956201+00:00\", \"payment_reference\": \"\", \"remarks\": \"Bulk wage payment for week 2025-11-03\", \"attendance_details\": {\"2025-11-03\": {\"status\": null, \"wage_rate\": 500.0, \"wage_earned\": 0.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, \"2025-11-04\": {\"status\": 1, \"wage_rate\": 500.0, \"wage_earned\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, \"2025-11-05\": {\"status\": null, \"wage_rate\": 500.0, \"wage_earned\": 0.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, \"2025-11-06\": {\"status\": null, \"wage_rate\": 500.0, \"wage_earned\": 0.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, \"2025-11-07\": {\"status\": 1, \"wage_rate\": 500.0, \"wage_earned\": 500.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, \"2025-11-08\": {\"status\": null, \"wage_rate\": 500.0, \"wage_earned\": 0.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}, \"2025-11-09\": {\"status\": null, \"wage_rate\": 500.0, \"wage_earned\": 0.0, \"wage_effective_from\": \"2024-07-01\", \"wage_effective_to\": \"2027-12-31\"}}, \"last_payment_date\": null, \"payment_remarks\": \"\", \"historical_wage_calculation\": {\"enabled\": true, \"primary_wage_rate\": 500.0, \"effective_from\": \"2024-07-01\", \"effective_to\": \"2027-12-31\", \"daily_rates_used\": [500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0], \"multiple_rates_in_week\": false, \"calculation_date\": \"2025-11-03\"}}]', 9, 13600.00, 13600.00, 13600.00, 0.00);

-- --------------------------------------------------------

--
-- Table structure for table `xe_yields`
--

CREATE TABLE `xe_yields` (
  `id` bigint(20) NOT NULL,
  `harvest_date` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `crop_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `xe_yields`
--

INSERT INTO `xe_yields` (`id`, `harvest_date`, `created_at`, `updated_at`, `crop_id`) VALUES
(200, '2024-11-06 00:00:00.000000', '2025-11-09 09:27:26.688551', '2025-11-09 09:27:26.688567', 3),
(201, '2024-12-22 00:00:00.000000', '2025-11-09 09:27:26.772723', '2025-11-09 09:27:26.772734', 4),
(202, '2025-05-25 00:00:00.000000', '2025-11-09 09:27:26.853819', '2025-11-09 09:27:26.853831', 5),
(203, '2025-07-02 00:00:00.000000', '2025-11-09 09:27:26.931200', '2025-11-09 09:27:26.931210', 7),
(204, '2025-01-11 00:00:00.000000', '2025-11-09 09:27:27.003076', '2025-11-09 09:27:27.003087', 5),
(205, '2024-06-06 00:00:00.000000', '2025-11-09 09:27:27.077658', '2025-11-09 09:27:27.077669', 5),
(206, '2024-11-10 00:00:00.000000', '2025-11-09 09:27:27.149948', '2025-11-09 09:27:27.149958', 4),
(207, '2025-04-09 00:00:00.000000', '2025-11-09 09:27:27.244119', '2025-11-09 09:27:27.244131', 5),
(208, '2025-03-09 00:00:00.000000', '2025-11-09 09:27:27.315508', '2025-11-09 09:27:27.315518', 4),
(209, '2025-06-08 00:00:00.000000', '2025-11-09 09:27:27.389871', '2025-11-09 09:27:27.389881', 3),
(210, '2025-09-07 00:00:00.000000', '2025-11-09 09:27:27.459364', '2025-11-09 09:27:27.459374', 4),
(211, '2024-11-24 00:00:00.000000', '2025-11-09 09:27:27.528379', '2025-11-09 09:27:27.528390', 7),
(212, '2025-03-09 00:00:00.000000', '2025-11-09 09:27:27.593366', '2025-11-09 09:27:27.593376', 5),
(213, '2024-06-28 00:00:00.000000', '2025-11-09 09:27:27.662377', '2025-11-09 09:27:27.662389', 5),
(214, '2024-07-20 00:00:00.000000', '2025-11-09 09:27:27.737061', '2025-11-09 09:27:27.737072', 5),
(215, '2024-07-15 00:00:00.000000', '2025-11-09 09:27:27.823796', '2025-11-09 09:27:27.823807', 5),
(216, '2025-05-04 00:00:00.000000', '2025-11-09 09:27:27.903022', '2025-11-09 09:27:27.903033', 3),
(217, '2024-07-17 00:00:00.000000', '2025-11-09 09:27:27.980261', '2025-11-09 09:27:27.980272', 5),
(218, '2025-08-20 00:00:00.000000', '2025-11-09 09:27:28.052694', '2025-11-09 09:27:28.052705', 4),
(219, '2024-12-04 00:00:00.000000', '2025-11-09 09:27:28.135306', '2025-11-09 09:27:28.135317', 3),
(220, '2025-01-03 13:12:00.000000', '2025-11-09 09:27:28.216097', '2025-11-09 09:27:28.216107', 3),
(221, '2025-01-24 00:00:00.000000', '2025-11-09 09:27:28.293520', '2025-11-09 09:27:28.293531', 3),
(222, '2025-04-06 08:22:00.000000', '2025-11-09 09:27:28.368051', '2025-11-09 09:27:28.368062', 4),
(223, '2024-08-10 00:00:00.000000', '2025-11-09 09:27:28.438650', '2025-11-09 09:27:28.438667', 5),
(224, '2024-06-29 00:00:00.000000', '2025-11-09 09:27:28.505115', '2025-11-09 09:27:28.505126', 4),
(225, '2024-12-18 00:00:00.000000', '2025-11-09 09:27:28.575327', '2025-11-09 09:27:28.575338', 3),
(226, '2024-06-29 00:00:00.000000', '2025-11-09 09:27:28.643847', '2025-11-09 09:27:28.643858', 3),
(227, '2025-07-20 08:21:00.000000', '2025-11-09 09:27:28.720282', '2025-11-09 09:27:28.720307', 3),
(228, '2025-08-03 00:00:00.000000', '2025-11-09 09:27:28.793463', '2025-11-09 09:27:28.793475', 7),
(229, '2025-01-19 00:00:00.000000', '2025-11-09 09:27:28.870581', '2025-11-09 09:27:28.870600', 3),
(230, '2025-09-07 00:00:00.000000', '2025-11-09 09:27:28.953917', '2025-11-09 09:27:28.953928', 3),
(231, '2024-12-10 00:00:00.000000', '2025-11-09 09:27:29.040223', '2025-11-09 09:27:29.040233', 4),
(232, '2025-03-23 00:00:00.000000', '2025-11-09 09:27:29.105517', '2025-11-09 09:27:29.105529', 4),
(233, '2025-02-09 00:00:00.000000', '2025-11-09 09:27:29.175651', '2025-11-09 09:27:29.175662', 3),
(234, '2024-12-20 00:00:00.000000', '2025-11-09 09:27:29.244518', '2025-11-09 09:27:29.244529', 3),
(235, '2024-07-20 00:00:00.000000', '2025-11-09 09:27:29.311137', '2025-11-09 09:27:29.311148', 4),
(236, '2025-06-01 00:00:00.000000', '2025-11-09 09:27:29.380943', '2025-11-09 09:27:29.380954', 3),
(237, '2025-01-04 15:37:00.000000', '2025-11-09 09:27:29.449375', '2025-11-09 09:27:29.449387', 4),
(238, '2025-06-25 11:08:00.000000', '2025-11-09 09:27:29.516967', '2025-11-09 09:27:29.516978', 3),
(239, '2025-04-27 00:00:00.000000', '2025-11-09 09:27:29.593793', '2025-11-09 09:27:29.593803', 3),
(240, '2024-12-08 00:00:00.000000', '2025-11-09 09:27:29.668909', '2025-11-09 09:27:29.668921', 3),
(241, '2025-08-20 00:00:00.000000', '2025-11-09 09:27:29.743264', '2025-11-09 09:27:29.743275', 3),
(242, '2025-03-09 00:00:00.000000', '2025-11-09 09:27:29.817278', '2025-11-09 09:27:29.817297', 3),
(243, '2024-12-15 00:00:00.000000', '2025-11-09 09:27:29.891530', '2025-11-09 09:27:29.891540', 3),
(244, '2025-08-20 00:00:00.000000', '2025-11-09 09:27:29.964424', '2025-11-09 09:27:29.964436', 5),
(245, '2024-12-11 00:00:00.000000', '2025-11-09 09:27:30.035593', '2025-11-09 09:27:30.035605', 3),
(246, '2025-08-03 17:35:00.000000', '2025-11-09 09:27:30.104455', '2025-11-09 09:27:30.104465', 3),
(247, '2024-10-07 00:00:00.000000', '2025-11-09 09:27:30.178335', '2025-11-09 09:27:30.178345', 4),
(248, '2024-11-13 09:27:00.000000', '2025-11-09 09:27:30.252322', '2025-11-09 09:27:30.252332', 3),
(249, '2025-05-04 00:00:00.000000', '2025-11-09 09:27:30.325216', '2025-11-09 09:27:30.325228', 4),
(250, '2025-02-01 00:00:00.000000', '2025-11-09 09:27:30.396585', '2025-11-09 09:27:30.396595', 4),
(251, '2025-05-18 00:00:00.000000', '2025-11-09 09:27:30.468385', '2025-11-09 09:27:30.468395', 4),
(252, '2024-11-24 00:00:00.000000', '2025-11-09 09:27:30.542790', '2025-11-09 09:27:30.542801', 3),
(253, '2025-02-19 11:26:00.000000', '2025-11-09 09:27:30.616279', '2025-11-09 09:27:30.616297', 4),
(254, '2025-05-25 00:00:00.000000', '2025-11-09 09:27:30.690386', '2025-11-09 09:27:30.690397', 4),
(255, '2025-04-27 00:00:00.000000', '2025-11-09 09:27:30.759554', '2025-11-09 09:27:30.759565', 4),
(256, '2025-07-11 00:00:00.000000', '2025-11-09 09:27:30.825599', '2025-11-09 09:27:30.825609', 3),
(257, '2025-04-20 00:00:00.000000', '2025-11-09 09:27:30.891666', '2025-11-09 09:27:30.891677', 4),
(258, '2024-07-20 00:00:00.000000', '2025-11-09 09:27:30.959012', '2025-11-09 09:27:30.959023', 7),
(259, '2025-09-14 00:00:00.000000', '2025-11-09 09:27:31.030499', '2025-11-09 09:27:31.030510', 4),
(260, '2025-04-12 09:30:00.000000', '2025-11-09 09:27:31.105482', '2025-11-09 09:27:31.105493', 3),
(261, '2025-04-25 09:06:00.000000', '2025-11-09 09:27:31.179841', '2025-11-09 09:27:31.179853', 5),
(262, '2024-11-17 00:00:00.000000', '2025-11-09 09:27:31.253788', '2025-11-09 09:27:31.253799', 3),
(263, '2025-06-25 11:10:00.000000', '2025-11-09 09:27:31.325483', '2025-11-09 09:27:31.325494', 5),
(264, '2025-08-03 00:00:00.000000', '2025-11-09 09:27:31.391561', '2025-11-09 09:27:31.391574', 5),
(265, '2025-01-10 00:00:00.000000', '2025-11-09 09:27:31.521674', '2025-11-09 09:27:31.521686', 3),
(266, '2025-04-20 00:00:00.000000', '2025-11-09 09:27:31.596966', '2025-11-09 09:27:31.596977', 3),
(267, '2025-07-23 00:00:00.000000', '2025-11-09 09:27:31.663938', '2025-11-09 09:27:31.663950', 5),
(268, '2025-02-07 00:00:00.000000', '2025-11-09 09:27:31.728388', '2025-11-09 09:27:31.728400', 9),
(269, '2025-09-14 00:00:00.000000', '2025-11-09 09:27:31.794333', '2025-11-09 09:27:31.794344', 5),
(270, '2024-08-10 00:00:00.000000', '2025-11-09 09:27:31.859670', '2025-11-09 09:27:31.859681', 4),
(271, '2025-05-18 00:00:00.000000', '2025-11-09 09:27:31.929752', '2025-11-09 09:27:31.929763', 3),
(272, '2025-02-01 00:00:00.000000', '2025-11-09 09:27:32.010509', '2025-11-09 09:27:32.010521', 5),
(273, '2025-01-08 17:39:00.000000', '2025-11-09 09:27:32.084274', '2025-11-09 09:27:32.084286', 3),
(274, '2025-01-31 00:00:00.000000', '2025-11-09 09:27:32.160364', '2025-11-09 09:27:32.160375', 3),
(275, '2025-03-16 08:34:00.000000', '2025-11-09 09:27:32.245228', '2025-11-09 09:27:32.245240', 3),
(276, '2024-06-01 00:00:00.000000', '2025-11-09 09:27:32.332751', '2025-11-09 09:27:32.332762', 8),
(277, '2025-04-13 00:00:00.000000', '2025-11-09 09:27:32.405982', '2025-11-09 09:27:32.405993', 4),
(278, '2025-06-25 11:10:00.000000', '2025-11-09 09:27:32.479511', '2025-11-09 09:27:32.479522', 4),
(279, '2024-07-17 00:00:00.000000', '2025-11-09 09:27:32.548367', '2025-11-09 09:27:32.548379', 3),
(280, '2025-04-20 00:00:00.000000', '2025-11-09 09:27:32.620985', '2025-11-09 09:27:32.620996', 7),
(281, '2024-06-17 00:00:00.000000', '2025-11-09 09:27:32.689149', '2025-11-09 09:27:32.689160', 4),
(282, '2025-04-13 00:00:00.000000', '2025-11-09 09:27:32.759538', '2025-11-09 09:27:32.759549', 5),
(283, '2025-07-02 00:00:00.000000', '2025-11-09 09:27:32.826100', '2025-11-09 09:27:32.826110', 4),
(284, '2025-02-19 11:27:00.000000', '2025-11-09 09:27:32.895815', '2025-11-09 09:27:32.895827', 5),
(285, '2025-07-06 00:00:00.000000', '2025-11-09 09:27:32.962524', '2025-11-09 09:27:32.962536', 5),
(286, '2025-07-06 00:00:00.000000', '2025-11-09 09:27:33.028654', '2025-11-09 09:27:33.028666', 4),
(287, '2024-07-17 00:00:00.000000', '2025-11-09 09:27:33.099871', '2025-11-09 09:27:33.099883', 4),
(288, '2025-03-23 00:00:00.000000', '2025-11-09 09:27:33.182258', '2025-11-09 09:27:33.182270', 3),
(289, '2025-05-06 00:00:00.000000', '2025-11-09 09:27:33.257110', '2025-11-09 09:27:33.257120', 5),
(290, '2024-12-25 00:00:00.000000', '2025-11-09 09:27:33.329554', '2025-11-09 09:27:33.329565', 3),
(291, '2025-09-14 00:00:00.000000', '2025-11-09 09:27:33.401461', '2025-11-09 09:27:33.401471', 3);

-- --------------------------------------------------------

--
-- Table structure for table `xe_yield_farm_segments`
--

CREATE TABLE `xe_yield_farm_segments` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `farm_segment_id` bigint(20) NOT NULL,
  `yield_record_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `xe_yield_farm_segments`
--

INSERT INTO `xe_yield_farm_segments` (`id`, `created_at`, `farm_segment_id`, `yield_record_id`) VALUES
(281, '2025-11-09 09:27:26.689706', 3, 200),
(282, '2025-11-09 09:27:26.773415', 3, 201),
(283, '2025-11-09 09:27:26.854613', 8, 202),
(284, '2025-11-09 09:27:26.931876', 8, 203),
(285, '2025-11-09 09:27:27.003841', 3, 204),
(286, '2025-11-09 09:27:27.078401', 3, 205),
(287, '2025-11-09 09:27:27.150633', 5, 206),
(288, '2025-11-09 09:27:27.244993', 8, 207),
(289, '2025-11-09 09:27:27.316221', 8, 208),
(290, '2025-11-09 09:27:27.390674', 8, 209),
(291, '2025-11-09 09:27:27.390695', 7, 209),
(292, '2025-11-09 09:27:27.460051', 5, 210),
(293, '2025-11-09 09:27:27.529159', 3, 211),
(294, '2025-11-09 09:27:27.594106', 8, 212),
(295, '2025-11-09 09:27:27.663176', 5, 213),
(296, '2025-11-09 09:27:27.737811', 7, 214),
(297, '2025-11-09 09:27:27.824695', 5, 215),
(298, '2025-11-09 09:27:27.903756', 7, 216),
(299, '2025-11-09 09:27:27.981043', 5, 217),
(300, '2025-11-09 09:27:28.053475', 7, 218),
(301, '2025-11-09 09:27:28.136003', 3, 219),
(302, '2025-11-09 09:27:28.216828', 8, 220),
(303, '2025-11-09 09:27:28.294313', 8, 221),
(304, '2025-11-09 09:27:28.368886', 8, 222),
(305, '2025-11-09 09:27:28.439455', 5, 223),
(306, '2025-11-09 09:27:28.505893', 5, 224),
(307, '2025-11-09 09:27:28.576099', 7, 225),
(308, '2025-11-09 09:27:28.644565', 5, 226),
(309, '2025-11-09 09:27:28.721132', 7, 227),
(310, '2025-11-09 09:27:28.794216', 7, 228),
(311, '2025-11-09 09:27:28.871495', 7, 229),
(312, '2025-11-09 09:27:28.954704', 5, 230),
(313, '2025-11-09 09:27:29.040921', 3, 231),
(314, '2025-11-09 09:27:29.106271', 8, 232),
(315, '2025-11-09 09:27:29.176405', 7, 233),
(316, '2025-11-09 09:27:29.245308', 7, 234),
(317, '2025-11-09 09:27:29.311837', 7, 235),
(318, '2025-11-09 09:27:29.381677', 7, 236),
(319, '2025-11-09 09:27:29.450148', 8, 237),
(320, '2025-11-09 09:27:29.517689', 8, 238),
(321, '2025-11-09 09:27:29.517709', 7, 238),
(322, '2025-11-09 09:27:29.594523', 7, 239),
(323, '2025-11-09 09:27:29.669700', 7, 240),
(324, '2025-11-09 09:27:29.744038', 5, 241),
(325, '2025-11-09 09:27:29.818056', 8, 242),
(326, '2025-11-09 09:27:29.892266', 7, 243),
(327, '2025-11-09 09:27:29.965236', 5, 244),
(328, '2025-11-09 09:27:30.036327', 7, 245),
(329, '2025-11-09 09:27:30.105144', 7, 246),
(330, '2025-11-09 09:27:30.179034', 5, 247),
(331, '2025-11-09 09:27:30.253001', 5, 248),
(332, '2025-11-09 09:27:30.325950', 3, 249),
(333, '2025-11-09 09:27:30.397268', 7, 250),
(334, '2025-11-09 09:27:30.469087', 8, 251),
(335, '2025-11-09 09:27:30.469106', 3, 251),
(336, '2025-11-09 09:27:30.543526', 5, 252),
(337, '2025-11-09 09:27:30.617026', 3, 253),
(338, '2025-11-09 09:27:30.691173', 8, 254),
(339, '2025-11-09 09:27:30.760445', 3, 255),
(340, '2025-11-09 09:27:30.826271', 7, 256),
(341, '2025-11-09 09:27:30.892361', 7, 257),
(342, '2025-11-09 09:27:30.959741', 7, 258),
(343, '2025-11-09 09:27:31.031258', 5, 259),
(344, '2025-11-09 09:27:31.106239', 7, 260),
(345, '2025-11-09 09:27:31.180660', 8, 261),
(346, '2025-11-09 09:27:31.254504', 5, 262),
(347, '2025-11-09 09:27:31.326258', 5, 263),
(348, '2025-11-09 09:27:31.392434', 5, 264),
(349, '2025-11-09 09:27:31.522446', 7, 265),
(350, '2025-11-09 09:27:31.597732', 7, 266),
(351, '2025-11-09 09:27:31.664735', 7, 267),
(352, '2025-11-09 09:27:31.729147', 6, 268),
(353, '2025-11-09 09:27:31.795339', 5, 269),
(354, '2025-11-09 09:27:31.860452', 5, 270),
(355, '2025-11-09 09:27:31.930502', 7, 271),
(356, '2025-11-09 09:27:32.011294', 7, 272),
(357, '2025-11-09 09:27:32.085096', 7, 273),
(358, '2025-11-09 09:27:32.161132', 7, 274),
(359, '2025-11-09 09:27:32.246325', 7, 275),
(360, '2025-11-09 09:27:32.334279', 5, 276),
(361, '2025-11-09 09:27:32.406909', 7, 277),
(362, '2025-11-09 09:27:32.480925', 8, 278),
(363, '2025-11-09 09:27:32.556564', 5, 279),
(364, '2025-11-09 09:27:32.621749', 7, 280),
(365, '2025-11-09 09:27:32.692254', 3, 281),
(366, '2025-11-09 09:27:32.760326', 7, 282),
(367, '2025-11-09 09:27:32.827257', 8, 283),
(368, '2025-11-09 09:27:32.896756', 5, 284),
(369, '2025-11-09 09:27:32.963516', 5, 285),
(370, '2025-11-09 09:27:33.029694', 8, 286),
(371, '2025-11-09 09:27:33.101049', 5, 287),
(372, '2025-11-09 09:27:33.183389', 7, 288),
(373, '2025-11-09 09:27:33.258300', 5, 289),
(374, '2025-11-09 09:27:33.330696', 6, 290),
(375, '2025-11-09 09:27:33.402309', 5, 291);

-- --------------------------------------------------------

--
-- Table structure for table `xe_yield_variants`
--

CREATE TABLE `xe_yield_variants` (
  `id` bigint(20) NOT NULL,
  `quantity` decimal(10,2) NOT NULL,
  `unit` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `crop_variant_id` bigint(20) NOT NULL,
  `yield_record_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `xe_yield_variants`
--

INSERT INTO `xe_yield_variants` (`id`, `quantity`, `unit`, `created_at`, `crop_variant_id`, `yield_record_id`) VALUES
(475, 3.00, 'Pack', '2025-11-09 09:27:26.690944', 5, 200),
(476, 2.00, 'Pack', '2025-11-09 09:27:26.690977', 7, 200),
(477, 1.00, 'Pack', '2025-11-09 09:27:26.690995', 9, 200),
(478, 1.00, 'Pack', '2025-11-09 09:27:26.691011', 8, 200),
(479, 44.00, 'Bunch', '2025-11-09 09:27:26.774421', 10, 201),
(480, 5.00, 'Bunch', '2025-11-09 09:27:26.774447', 11, 201),
(481, 59.00, 'Pieces', '2025-11-09 09:27:26.855615', 13, 202),
(482, 120.00, 'Pieces', '2025-11-09 09:27:26.932832', 12, 203),
(483, 10.00, 'Pieces', '2025-11-09 09:27:27.004843', 13, 204),
(484, 23.00, 'Pieces', '2025-11-09 09:27:27.079513', 13, 205),
(485, 60.00, 'Bunch', '2025-11-09 09:27:27.151610', 10, 206),
(486, 6.00, 'Bunch', '2025-11-09 09:27:27.151634', 11, 206),
(487, 32.00, 'Pieces', '2025-11-09 09:27:27.246083', 13, 207),
(488, 10.00, 'Bunch', '2025-11-09 09:27:27.317212', 10, 208),
(489, 5.00, 'Bunch', '2025-11-09 09:27:27.317236', 11, 208),
(490, 1.00, 'Pack', '2025-11-09 09:27:27.391880', 5, 209),
(491, 3.00, 'Pack', '2025-11-09 09:27:27.391904', 8, 209),
(492, 2.00, 'Pack', '2025-11-09 09:27:27.391921', 7, 209),
(493, 1.00, 'Pack', '2025-11-09 09:27:27.391936', 6, 209),
(494, 2.00, 'Pack', '2025-11-09 09:27:27.391950', 9, 209),
(495, 10.00, 'Bunch', '2025-11-09 09:27:27.461042', 10, 210),
(496, 5.00, 'Bunch', '2025-11-09 09:27:27.461072', 11, 210),
(497, 400.00, 'Pieces', '2025-11-09 09:27:27.530160', 12, 211),
(498, 33.00, 'Pieces', '2025-11-09 09:27:27.595101', 13, 212),
(499, 50.00, 'Pieces', '2025-11-09 09:27:27.664215', 13, 213),
(500, 54.00, 'Pieces', '2025-11-09 09:27:27.738783', 13, 214),
(501, 80.00, 'Pieces', '2025-11-09 09:27:27.825668', 13, 215),
(502, 1.00, 'Pack', '2025-11-09 09:27:27.904802', 5, 216),
(503, 1.00, 'Pack', '2025-11-09 09:27:27.904827', 7, 216),
(504, 1.00, 'Pack', '2025-11-09 09:27:27.904845', 6, 216),
(505, 1.00, 'Pack', '2025-11-09 09:27:27.904859', 9, 216),
(506, 1.00, 'Pack', '2025-11-09 09:27:27.904873', 8, 216),
(507, 13.00, 'Pieces', '2025-11-09 09:27:27.982033', 13, 217),
(508, 1.00, 'Bunch', '2025-11-09 09:27:28.054504', 11, 218),
(509, 9.00, 'Bunch', '2025-11-09 09:27:28.054527', 10, 218),
(510, 6.00, 'Pack', '2025-11-09 09:27:28.137052', 5, 219),
(511, 2.00, 'Pack', '2025-11-09 09:27:28.137077', 7, 219),
(512, 1.00, 'Pack', '2025-11-09 09:27:28.137093', 9, 219),
(513, 1.00, 'Pack', '2025-11-09 09:27:28.137108', 8, 219),
(514, 1.00, 'Pack', '2025-11-09 09:27:28.137122', 6, 219),
(515, 4.00, 'Pack', '2025-11-09 09:27:28.217850', 5, 220),
(516, 1.00, 'Pack', '2025-11-09 09:27:28.217876', 7, 220),
(517, 3.00, 'Pack', '2025-11-09 09:27:28.217891', 9, 220),
(518, 3.00, 'Pack', '2025-11-09 09:27:28.295359', 5, 221),
(519, 1.00, 'Pack', '2025-11-09 09:27:28.295384', 7, 221),
(520, 1.00, 'Pack', '2025-11-09 09:27:28.295401', 6, 221),
(521, 3.00, 'Pack', '2025-11-09 09:27:28.295415', 9, 221),
(522, 17.00, 'Bunch', '2025-11-09 09:27:28.369945', 10, 222),
(523, 4.00, 'Bunch', '2025-11-09 09:27:28.369972', 11, 222),
(524, 46.00, 'Pieces', '2025-11-09 09:27:28.440482', 13, 223),
(525, 17.00, 'Bunch', '2025-11-09 09:27:28.506911', 11, 224),
(526, 4.00, 'Pack', '2025-11-09 09:27:28.577169', 5, 225),
(527, 1.00, 'Pack', '2025-11-09 09:27:28.577194', 7, 225),
(528, 1.00, 'Pack', '2025-11-09 09:27:28.577217', 6, 225),
(529, 3.00, 'Pack', '2025-11-09 09:27:28.577235', 9, 225),
(530, 1.00, 'Pack', '2025-11-09 09:27:28.577249', 8, 225),
(531, 3.00, 'Pack', '2025-11-09 09:27:28.645553', 7, 226),
(532, 1.00, 'Pack', '2025-11-09 09:27:28.722192', 5, 227),
(533, 1.00, 'Pack', '2025-11-09 09:27:28.722216', 7, 227),
(534, 1.00, 'Pack', '2025-11-09 09:27:28.722232', 8, 227),
(535, 1.00, 'Pack', '2025-11-09 09:27:28.722248', 9, 227),
(536, 252.00, 'Pieces', '2025-11-09 09:27:28.795209', 12, 228),
(537, 3.00, 'Pack', '2025-11-09 09:27:28.872626', 5, 229),
(538, 1.00, 'Pack', '2025-11-09 09:27:28.872651', 6, 229),
(539, 1.00, 'Pack', '2025-11-09 09:27:28.872672', 7, 229),
(540, 3.00, 'Pack', '2025-11-09 09:27:28.872701', 8, 229),
(541, 2.00, 'Pack', '2025-11-09 09:27:28.872732', 9, 229),
(542, 1.00, 'Pack', '2025-11-09 09:27:28.955799', 5, 230),
(543, 1.00, 'Pack', '2025-11-09 09:27:28.955824', 7, 230),
(544, 1.00, 'Pack', '2025-11-09 09:27:28.955841', 6, 230),
(545, 1.00, 'Pack', '2025-11-09 09:27:28.955857', 9, 230),
(546, 1.00, 'Pack', '2025-11-09 09:27:28.955871', 8, 230),
(547, 16.00, 'Bunch', '2025-11-09 09:27:29.041899', 10, 231),
(548, 12.00, 'Pack', '2025-11-09 09:27:29.107279', 10, 232),
(549, 3.00, 'Pack', '2025-11-09 09:27:29.107311', 11, 232),
(550, 1.00, 'Pack', '2025-11-09 09:27:29.177470', 5, 233),
(551, 2.00, 'Pack', '2025-11-09 09:27:29.177494', 7, 233),
(552, 2.00, 'Pack', '2025-11-09 09:27:29.177510', 8, 233),
(553, 2.00, 'Pack', '2025-11-09 09:27:29.177525', 9, 233),
(554, 4.00, 'Pack', '2025-11-09 09:27:29.246353', 5, 234),
(555, 1.00, 'Pack', '2025-11-09 09:27:29.246377', 7, 234),
(556, 2.00, 'Pack', '2025-11-09 09:27:29.246394', 9, 234),
(557, 10.00, 'Bunch', '2025-11-09 09:27:29.312797', 11, 235),
(558, 2.00, 'Pack', '2025-11-09 09:27:29.382736', 5, 236),
(559, 1.00, 'Pack', '2025-11-09 09:27:29.382761', 7, 236),
(560, 2.00, 'Pack', '2025-11-09 09:27:29.382778', 9, 236),
(561, 1.00, 'Pack', '2025-11-09 09:27:29.382794', 6, 236),
(562, 1.00, 'Pack', '2025-11-09 09:27:29.382808', 8, 236),
(563, 15.00, 'Bunch', '2025-11-09 09:27:29.451193', 10, 237),
(564, 2.00, 'Bunch', '2025-11-09 09:27:29.451218', 11, 237),
(565, 1.00, 'Pack', '2025-11-09 09:27:29.518740', 5, 238),
(566, 4.00, 'Pack', '2025-11-09 09:27:29.518765', 8, 238),
(567, 2.00, 'Pack', '2025-11-09 09:27:29.518781', 7, 238),
(568, 3.00, 'Pack', '2025-11-09 09:27:29.518796', 9, 238),
(569, 1.00, 'Pack', '2025-11-09 09:27:29.595578', 5, 239),
(570, 1.00, 'Pack', '2025-11-09 09:27:29.595601', 7, 239),
(571, 1.00, 'Pack', '2025-11-09 09:27:29.595616', 6, 239),
(572, 1.00, 'Pack', '2025-11-09 09:27:29.595630', 9, 239),
(573, 6.00, 'Pack', '2025-11-09 09:27:29.670749', 5, 240),
(574, 2.00, 'Pack', '2025-11-09 09:27:29.670775', 7, 240),
(575, 3.00, 'Pack', '2025-11-09 09:27:29.670792', 9, 240),
(576, 1.00, 'Pack', '2025-11-09 09:27:29.745092', 5, 241),
(577, 2.00, 'Pack', '2025-11-09 09:27:29.745118', 7, 241),
(578, 1.00, 'Pack', '2025-11-09 09:27:29.745135', 9, 241),
(579, 2.00, 'Bunch', '2025-11-09 09:27:29.819055', 8, 242),
(580, 2.00, 'Pack', '2025-11-09 09:27:29.893301', 5, 243),
(581, 1.00, 'Pack', '2025-11-09 09:27:29.893324', 7, 243),
(582, 1.00, 'Pack', '2025-11-09 09:27:29.893340', 9, 243),
(583, 17.00, 'Pieces', '2025-11-09 09:27:29.966246', 13, 244),
(584, 3.00, 'Pack', '2025-11-09 09:27:30.037367', 5, 245),
(585, 1.00, 'Pack', '2025-11-09 09:27:30.037391', 7, 245),
(586, 2.00, 'Pack', '2025-11-09 09:27:30.037406', 9, 245),
(587, 1.00, 'Pack', '2025-11-09 09:27:30.106166', 5, 246),
(588, 1.00, 'Pack', '2025-11-09 09:27:30.106189', 7, 246),
(589, 2.00, 'Pack', '2025-11-09 09:27:30.106204', 9, 246),
(590, 1.00, 'Pack', '2025-11-09 09:27:30.106217', 8, 246),
(591, 1.00, 'Pack', '2025-11-09 09:27:30.106230', 6, 246),
(592, 19.00, 'Bunch', '2025-11-09 09:27:30.180039', 10, 247),
(593, 11.00, 'Bunch', '2025-11-09 09:27:30.180065', 11, 247),
(594, 4.00, 'Pack', '2025-11-09 09:27:30.254019', 5, 248),
(595, 2.00, 'Pack', '2025-11-09 09:27:30.254045', 7, 248),
(596, 2.00, 'Pack', '2025-11-09 09:27:30.254061', 8, 248),
(597, 2.00, 'Pack', '2025-11-09 09:27:30.254076', 9, 248),
(598, 10.00, 'Bunch', '2025-11-09 09:27:30.326946', 10, 249),
(599, 8.00, 'Bunch', '2025-11-09 09:27:30.398263', 11, 250),
(600, 8.00, 'Bunch', '2025-11-09 09:27:30.398288', 10, 250),
(601, 10.00, 'Bunch', '2025-11-09 09:27:30.470124', 10, 251),
(602, 5.00, 'Bunch', '2025-11-09 09:27:30.470148', 11, 251),
(603, 5.00, 'Pack', '2025-11-09 09:27:30.544538', 5, 252),
(604, 1.00, 'Pack', '2025-11-09 09:27:30.544563', 7, 252),
(605, 1.00, 'Pack', '2025-11-09 09:27:30.544580', 9, 252),
(606, 11.00, 'Bunch', '2025-11-09 09:27:30.618024', 10, 253),
(607, 12.00, 'Bunch', '2025-11-09 09:27:30.692229', 10, 254),
(608, 10.00, 'Bunch', '2025-11-09 09:27:30.761466', 10, 255),
(609, 2.00, 'Pieces', '2025-11-09 09:27:30.761490', 11, 255),
(610, 1.00, 'Pack', '2025-11-09 09:27:30.827268', 5, 256),
(611, 1.00, 'Pack', '2025-11-09 09:27:30.827298', 9, 256),
(612, 1.00, 'Pack', '2025-11-09 09:27:30.827314', 8, 256),
(613, 11.00, 'Bunch', '2025-11-09 09:27:30.893324', 10, 257),
(614, 700.00, 'Pieces', '2025-11-09 09:27:30.960739', 12, 258),
(615, 8.00, 'Bunch', '2025-11-09 09:27:31.032303', 10, 259),
(616, 3.00, 'Bunch', '2025-11-09 09:27:31.032328', 11, 259),
(617, 3.00, 'Bunch', '2025-11-09 09:27:31.107274', 5, 260),
(618, 2.00, 'Bunch', '2025-11-09 09:27:31.107308', 7, 260),
(619, 2.00, 'Bunch', '2025-11-09 09:27:31.107326', 9, 260),
(620, 40.00, 'Pieces', '2025-11-09 09:27:31.181682', 13, 261),
(621, 2.00, 'Pack', '2025-11-09 09:27:31.255539', 5, 262),
(622, 1.00, 'Pack', '2025-11-09 09:27:31.255564', 8, 262),
(623, 1.00, 'Pack', '2025-11-09 09:27:31.255581', 7, 262),
(624, 2.00, 'Pack', '2025-11-09 09:27:31.255596', 9, 262),
(625, 30.00, 'Pieces', '2025-11-09 09:27:31.327262', 13, 263),
(626, 24.00, 'Pieces', '2025-11-09 09:27:31.393534', 13, 264),
(627, 3.00, 'Pack', '2025-11-09 09:27:31.523513', 5, 265),
(628, 2.00, 'Pack', '2025-11-09 09:27:31.523538', 9, 265),
(629, 1.00, 'Pack', '2025-11-09 09:27:31.523555', 7, 265),
(630, 9.00, 'Pack', '2025-11-09 09:27:31.523569', 8, 265),
(631, 2.00, 'Pack', '2025-11-09 09:27:31.598789', 5, 266),
(632, 2.00, 'Pack', '2025-11-09 09:27:31.598814', 7, 266),
(633, 1.00, 'Pack', '2025-11-09 09:27:31.598832', 8, 266),
(634, 2.00, 'Pack', '2025-11-09 09:27:31.598848', 9, 266),
(635, 63.00, 'Pieces', '2025-11-09 09:27:31.665742', 13, 267),
(636, 3.00, 'Pack', '2025-11-09 09:27:31.730139', 16, 268),
(637, 30.00, 'Pieces', '2025-11-09 09:27:31.796366', 13, 269),
(638, 23.00, 'Bunch', '2025-11-09 09:27:31.861454', 11, 270),
(639, 2.00, 'Pack', '2025-11-09 09:27:31.931566', 5, 271),
(640, 1.00, 'Pack', '2025-11-09 09:27:31.931592', 7, 271),
(641, 2.00, 'Pack', '2025-11-09 09:27:31.931609', 6, 271),
(642, 1.00, 'Pack', '2025-11-09 09:27:31.931624', 9, 271),
(643, 1.00, 'Pack', '2025-11-09 09:27:31.931638', 8, 271),
(644, 10.00, 'Pieces', '2025-11-09 09:27:32.012341', 13, 272),
(645, 4.00, 'Pack', '2025-11-09 09:27:32.086147', 5, 273),
(646, 2.00, 'Pack', '2025-11-09 09:27:32.086172', 7, 273),
(647, 2.00, 'Pack', '2025-11-09 09:27:32.086189', 9, 273),
(648, 2.00, 'Pack', '2025-11-09 09:27:32.162169', 5, 274),
(649, 2.00, 'Pack', '2025-11-09 09:27:32.162194', 7, 274),
(650, 4.00, 'Pack', '2025-11-09 09:27:32.162210', 8, 274),
(651, 3.00, 'Pack', '2025-11-09 09:27:32.162225', 9, 274),
(652, 3.00, 'Pack', '2025-11-09 09:27:32.247441', 5, 275),
(653, 1.00, 'Pack', '2025-11-09 09:27:32.247468', 7, 275),
(654, 1.00, 'Pack', '2025-11-09 09:27:32.247485', 8, 275),
(655, 1.00, 'Pack', '2025-11-09 09:27:32.247502', 9, 275),
(656, 1.00, 'Pack', '2025-11-09 09:27:32.335437', 18, 276),
(657, 18.00, 'Bunch', '2025-11-09 09:27:32.408076', 10, 277),
(658, 2.00, 'Bunch', '2025-11-09 09:27:32.408100', 11, 277),
(659, 2.00, 'Bunch', '2025-11-09 09:27:32.482061', 11, 278),
(660, 3.00, 'Pack', '2025-11-09 09:27:32.558142', 7, 279),
(661, 300.00, 'Pieces', '2025-11-09 09:27:32.622766', 12, 280),
(662, 23.00, 'Bunch', '2025-11-09 09:27:32.693278', 11, 281),
(663, 40.00, 'Pieces', '2025-11-09 09:27:32.761569', 13, 282),
(664, 3.00, 'Bunch', '2025-11-09 09:27:32.828307', 11, 283),
(665, 15.00, 'Bunch', '2025-11-09 09:27:32.828332', 10, 283),
(666, 22.00, 'Pieces', '2025-11-09 09:27:32.897838', 13, 284),
(667, 60.00, 'Pieces', '2025-11-09 09:27:32.964665', 13, 285),
(668, 8.00, 'Bunch', '2025-11-09 09:27:33.030852', 11, 286),
(669, 14.00, 'Bunch', '2025-11-09 09:27:33.102610', 11, 287),
(670, 2.00, 'Pack', '2025-11-09 09:27:33.184681', 5, 288),
(671, 1.00, 'Pack', '2025-11-09 09:27:33.184706', 7, 288),
(672, 1.00, 'Pack', '2025-11-09 09:27:33.184722', 9, 288),
(673, 1.00, 'Pack', '2025-11-09 09:27:33.184737', 8, 288),
(674, 57.00, 'Pieces', '2025-11-09 09:27:33.259568', 13, 289),
(675, 4.00, 'Pack', '2025-11-09 09:27:33.331869', 5, 290),
(676, 2.00, 'Pack', '2025-11-09 09:27:33.331893', 7, 290),
(677, 3.00, 'Pack', '2025-11-09 09:27:33.331910', 9, 290),
(678, 1.00, 'Pack', '2025-11-09 09:27:33.403439', 5, 291),
(679, 1.00, 'Pack', '2025-11-09 09:27:33.403464', 6, 291),
(680, 1.00, 'Pack', '2025-11-09 09:27:33.403482', 7, 291),
(681, 2.00, 'Pack', '2025-11-09 09:27:33.403498', 9, 291),
(682, 2.00, 'Pack', '2025-11-09 09:27:33.403512', 8, 291);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `bulk_wage_payments`
--
ALTER TABLE `bulk_wage_payments`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `bulk_wage_payments_week_start_date_week_end_date_1c769806_uniq` (`week_start_date`,`week_end_date`),
  ADD KEY `bulk_wage_payments_paid_by_id_039cc16a_fk_xe_employee_id` (`paid_by_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `farm_segments`
--
ALTER TABLE `farm_segments`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `xe_attendance_records`
--
ALTER TABLE `xe_attendance_records`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `date` (`date`),
  ADD KEY `xe_attendance_records_created_by_id_c5e26379_fk_xe_employee_id` (`created_by_id`);

--
-- Indexes for table `xe_attendance_weekly_summary`
--
ALTER TABLE `xe_attendance_weekly_summary`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `week_start_date` (`week_start_date`);

--
-- Indexes for table `xe_bill_images`
--
ALTER TABLE `xe_bill_images`
  ADD PRIMARY KEY (`id`),
  ADD KEY `xe_bill_images_yield_record_id_55ad2a0c_fk_xe_yields_id` (`yield_record_id`);

--
-- Indexes for table `xe_crops`
--
ALTER TABLE `xe_crops`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `xe_crop_variants`
--
ALTER TABLE `xe_crop_variants`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `xe_crop_variants_crop_id_crop_variant_6171c981_uniq` (`crop_id`,`crop_variant`);

--
-- Indexes for table `xe_employee`
--
ALTER TABLE `xe_employee`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `xe_expenses`
--
ALTER TABLE `xe_expenses`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `xe_farm_scrapedevent`
--
ALTER TABLE `xe_farm_scrapedevent`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `event_id` (`event_id`),
  ADD KEY `xe_farm_scr_start_d_ab0921_idx` (`start_datetime`),
  ADD KEY `xe_farm_scr_city_fca1f0_idx` (`city`,`country`),
  ADD KEY `xe_farm_scr_event_c_ffd0a5_idx` (`event_category`);

--
-- Indexes for table `xe_jobs`
--
ALTER TABLE `xe_jobs`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `xe_job_employees`
--
ALTER TABLE `xe_job_employees`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `xe_job_employees_job_id_employee_id_a0451d0b_uniq` (`job_id`,`employee_id`),
  ADD KEY `xe_job_employees_employee_id_ada564d5_fk_xe_employee_id` (`employee_id`);

--
-- Indexes for table `xe_job_farm_segments`
--
ALTER TABLE `xe_job_farm_segments`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `xe_job_farm_segments_job_id_farm_segment_id_1639e583_uniq` (`job_id`,`farm_segment_id`),
  ADD KEY `xe_job_farm_segments_farm_segment_id_228a48a2_fk_farm_segm` (`farm_segment_id`);

--
-- Indexes for table `xe_merchant`
--
ALTER TABLE `xe_merchant`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `contact` (`contact`);

--
-- Indexes for table `xe_payment_history`
--
ALTER TABLE `xe_payment_history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `xe_payment_history_sale_id_5b0a96fa_fk_xe_sales_id` (`sale_id`);

--
-- Indexes for table `xe_sales`
--
ALTER TABLE `xe_sales`
  ADD PRIMARY KEY (`id`),
  ADD KEY `xe_sales_yield_record_id_3e651923_fk_xe_yields_id` (`yield_record_id`),
  ADD KEY `xe_sales_merchant_id_ac1dd84c_fk_xe_merchant_id` (`merchant_id`);

--
-- Indexes for table `xe_sale_images`
--
ALTER TABLE `xe_sale_images`
  ADD PRIMARY KEY (`id`),
  ADD KEY `xe_sale_images_sale_id_bdee1638_fk_xe_sales_id` (`sale_id`);

--
-- Indexes for table `xe_sale_variants`
--
ALTER TABLE `xe_sale_variants`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `xe_sale_variants_sale_id_crop_variant_id_d8d42d0d_uniq` (`sale_id`,`crop_variant_id`),
  ADD KEY `xe_sale_variants_crop_variant_id_5c5fca54_fk_xe_crop_variants_id` (`crop_variant_id`);

--
-- Indexes for table `xe_wages`
--
ALTER TABLE `xe_wages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `xe_wages_employee_id_936e36f2_fk_xe_employee_id` (`employee_id`);

--
-- Indexes for table `xe_wage_payment_transactions`
--
ALTER TABLE `xe_wage_payment_transactions`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `xe_weekly_wage_payment`
--
ALTER TABLE `xe_weekly_wage_payment`
  ADD PRIMARY KEY (`id`),
  ADD KEY `xe_weekly_wage_payme_expense_entry_id_1ebdfcea_fk_xe_expens` (`expense_entry_id`);

--
-- Indexes for table `xe_yields`
--
ALTER TABLE `xe_yields`
  ADD PRIMARY KEY (`id`),
  ADD KEY `xe_yields_crop_id` (`crop_id`) USING BTREE;

--
-- Indexes for table `xe_yield_farm_segments`
--
ALTER TABLE `xe_yield_farm_segments`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `xe_yield_farm_segments_yield_record_id_farm_seg_1b016a9b_uniq` (`yield_record_id`,`farm_segment_id`),
  ADD KEY `xe_yield_farm_segmen_farm_segment_id_01c55662_fk_farm_segm` (`farm_segment_id`);

--
-- Indexes for table `xe_yield_variants`
--
ALTER TABLE `xe_yield_variants`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `xe_yield_variants_yield_record_id_crop_variant_id_34229b9b_uniq` (`yield_record_id`,`crop_variant_id`),
  ADD KEY `xe_yield_variants_crop_variant_id_6caac8a9_fk_xe_crop_v` (`crop_variant_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=121;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `bulk_wage_payments`
--
ALTER TABLE `bulk_wage_payments`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;

--
-- AUTO_INCREMENT for table `farm_segments`
--
ALTER TABLE `farm_segments`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `xe_attendance_records`
--
ALTER TABLE `xe_attendance_records`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=635;

--
-- AUTO_INCREMENT for table `xe_attendance_weekly_summary`
--
ALTER TABLE `xe_attendance_weekly_summary`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `xe_bill_images`
--
ALTER TABLE `xe_bill_images`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `xe_crops`
--
ALTER TABLE `xe_crops`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `xe_crop_variants`
--
ALTER TABLE `xe_crop_variants`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `xe_employee`
--
ALTER TABLE `xe_employee`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=64;

--
-- AUTO_INCREMENT for table `xe_expenses`
--
ALTER TABLE `xe_expenses`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=687;

--
-- AUTO_INCREMENT for table `xe_farm_scrapedevent`
--
ALTER TABLE `xe_farm_scrapedevent`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `xe_jobs`
--
ALTER TABLE `xe_jobs`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `xe_job_employees`
--
ALTER TABLE `xe_job_employees`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `xe_job_farm_segments`
--
ALTER TABLE `xe_job_farm_segments`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `xe_merchant`
--
ALTER TABLE `xe_merchant`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `xe_payment_history`
--
ALTER TABLE `xe_payment_history`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `xe_sales`
--
ALTER TABLE `xe_sales`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=176;

--
-- AUTO_INCREMENT for table `xe_sale_images`
--
ALTER TABLE `xe_sale_images`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `xe_sale_variants`
--
ALTER TABLE `xe_sale_variants`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=396;

--
-- AUTO_INCREMENT for table `xe_wages`
--
ALTER TABLE `xe_wages`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `xe_wage_payment_transactions`
--
ALTER TABLE `xe_wage_payment_transactions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `xe_weekly_wage_payment`
--
ALTER TABLE `xe_weekly_wage_payment`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT for table `xe_yields`
--
ALTER TABLE `xe_yields`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=293;

--
-- AUTO_INCREMENT for table `xe_yield_farm_segments`
--
ALTER TABLE `xe_yield_farm_segments`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=377;

--
-- AUTO_INCREMENT for table `xe_yield_variants`
--
ALTER TABLE `xe_yield_variants`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=684;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `bulk_wage_payments`
--
ALTER TABLE `bulk_wage_payments`
  ADD CONSTRAINT `bulk_wage_payments_paid_by_id_039cc16a_fk_xe_employee_id` FOREIGN KEY (`paid_by_id`) REFERENCES `xe_employee` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `xe_attendance_records`
--
ALTER TABLE `xe_attendance_records`
  ADD CONSTRAINT `xe_attendance_records_created_by_id_c5e26379_fk_xe_employee_id` FOREIGN KEY (`created_by_id`) REFERENCES `xe_employee` (`id`);

--
-- Constraints for table `xe_bill_images`
--
ALTER TABLE `xe_bill_images`
  ADD CONSTRAINT `xe_bill_images_yield_record_id_55ad2a0c_fk_xe_yields_id` FOREIGN KEY (`yield_record_id`) REFERENCES `xe_yields` (`id`);

--
-- Constraints for table `xe_crop_variants`
--
ALTER TABLE `xe_crop_variants`
  ADD CONSTRAINT `xe_crop_variants_crop_id_87dd85d1_fk_xe_crops_id` FOREIGN KEY (`crop_id`) REFERENCES `xe_crops` (`id`);

--
-- Constraints for table `xe_job_employees`
--
ALTER TABLE `xe_job_employees`
  ADD CONSTRAINT `xe_job_employees_employee_id_ada564d5_fk_xe_employee_id` FOREIGN KEY (`employee_id`) REFERENCES `xe_employee` (`id`),
  ADD CONSTRAINT `xe_job_employees_job_id_d9052f64_fk_xe_jobs_id` FOREIGN KEY (`job_id`) REFERENCES `xe_jobs` (`id`);

--
-- Constraints for table `xe_job_farm_segments`
--
ALTER TABLE `xe_job_farm_segments`
  ADD CONSTRAINT `xe_job_farm_segments_farm_segment_id_228a48a2_fk_farm_segm` FOREIGN KEY (`farm_segment_id`) REFERENCES `farm_segments` (`id`),
  ADD CONSTRAINT `xe_job_farm_segments_job_id_3ed949d5_fk_xe_jobs_id` FOREIGN KEY (`job_id`) REFERENCES `xe_jobs` (`id`);

--
-- Constraints for table `xe_payment_history`
--
ALTER TABLE `xe_payment_history`
  ADD CONSTRAINT `xe_payment_history_sale_id_5b0a96fa_fk_xe_sales_id` FOREIGN KEY (`sale_id`) REFERENCES `xe_sales` (`id`);

--
-- Constraints for table `xe_sales`
--
ALTER TABLE `xe_sales`
  ADD CONSTRAINT `xe_sales_merchant_id_ac1dd84c_fk_xe_merchant_id` FOREIGN KEY (`merchant_id`) REFERENCES `xe_merchant` (`id`),
  ADD CONSTRAINT `xe_sales_yield_record_id_3e651923_fk_xe_yields_id` FOREIGN KEY (`yield_record_id`) REFERENCES `xe_yields` (`id`);

--
-- Constraints for table `xe_sale_images`
--
ALTER TABLE `xe_sale_images`
  ADD CONSTRAINT `xe_sale_images_sale_id_bdee1638_fk_xe_sales_id` FOREIGN KEY (`sale_id`) REFERENCES `xe_sales` (`id`);

--
-- Constraints for table `xe_sale_variants`
--
ALTER TABLE `xe_sale_variants`
  ADD CONSTRAINT `xe_sale_variants_crop_variant_id_5c5fca54_fk_xe_crop_variants_id` FOREIGN KEY (`crop_variant_id`) REFERENCES `xe_crop_variants` (`id`),
  ADD CONSTRAINT `xe_sale_variants_sale_id_95ff2c26_fk_xe_sales_id` FOREIGN KEY (`sale_id`) REFERENCES `xe_sales` (`id`);

--
-- Constraints for table `xe_wages`
--
ALTER TABLE `xe_wages`
  ADD CONSTRAINT `xe_wages_employee_id_936e36f2_fk_xe_employee_id` FOREIGN KEY (`employee_id`) REFERENCES `xe_employee` (`id`);

--
-- Constraints for table `xe_weekly_wage_payment`
--
ALTER TABLE `xe_weekly_wage_payment`
  ADD CONSTRAINT `xe_weekly_wage_payme_expense_entry_id_1ebdfcea_fk_xe_expens` FOREIGN KEY (`expense_entry_id`) REFERENCES `xe_expenses` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `xe_yields`
--
ALTER TABLE `xe_yields`
  ADD CONSTRAINT `xe_yields_crop_id_e0290cc1_fk_xe_crops_id` FOREIGN KEY (`crop_id`) REFERENCES `xe_crops` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

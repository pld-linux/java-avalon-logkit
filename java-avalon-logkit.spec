#
# Conditional build:
%bcond_without	jms	# build output jms classes

%define		srcname	avalon-logkit
%include	/usr/lib/rpm/macros.java
Summary:	Java logging toolkit
Summary(pl.UTF-8):	Biblioteka do logowania w Javie
Name:		java-avalon-logkit
Version:	2.1
Release:	2
License:	Apache v2.0
Group:		Libraries/Java
Source0:	http://www.apache.org/dist/excalibur/avalon-logkit/source/%{srcname}-%{version}-src.tar.gz
# Source0-md5:	fee6f5f2db70c320aafbfb4cc32c1c43
Patch0:		%{name}-java7.patch
URL:		http://excalibur.apache.org/logger.html
BuildRequires:	ant
BuildRequires:	ant-junit
%if %(locale -a | grep -q ^en_US$ ; echo $?)
BuildRequires:	glibc-localedb-all
%endif
BuildRequires:	java(javamail)
BuildRequires:	java(jdbc-stdext)
BuildRequires:	java(servlet)
BuildRequires:	java-junit
BuildRequires:	java-log4j
BuildRequires:	jdk
%{?with_jms:BuildRequires:	jms}
BuildRequires:	jpackage-utils >= 0:1.5
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	java(jdbc-stdext)
Requires:	java(servlet)
%{?with_jms:Requires:	jms}
Obsoletes:	avalon-logkit
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LogKit is a logging toolkit designed for secure performance orientated
logging in applications. To get started using LogKit, it is recomended
that you read the whitepaper and browse the API docs.

%description -l pl.UTF-8
LogKit to biblioteka do logowania zaprojektowana z myślą o
bezpiecznym, wydajnym logowaniu w aplikacjach. Zaleca się zacząć
używanie LogKitu od przeczytania specyfikacji i przejrzenia
dokumentacji API.

%package javadoc
Summary:	Javadoc for Avalon LogKit
Summary(pl.UTF-8):	Dokumentacja Javadoc do pakietu Avalon LogKit
Group:		Documentation
Requires:	jpackage-utils
Obsoletes:	avalon-logkit-javadoc

%description javadoc
Javadoc for Avalon LogKit.

%description javadoc -l pl.UTF-8
Dokumentacja Javadoc do pakietu Avalon LogKit.

%prep
%setup -q -n %{srcname}-%{version}
%patch0 -p1

%build
required_jars="log4j mail %{?with_jms:jms} servlet-api jdbc-stdext junit"
PWD=$(pwd)
CLASSPATH=$(build-classpath $required_jars) #:$PWD/build/classes

export LC_ALL=en_US # source code not US-ASCII

%ant clean jar javadoc \
	-Dnoget=1

%install
rm -rf $RPM_BUILD_ROOT
# jars
install -d $RPM_BUILD_ROOT%{_javadir}
cp -a target/avalon-logkit-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%doc LICENSE.txt NOTICE.txt
%{_javadir}/avalon-logkit-%{version}.jar
%{_javadir}/avalon-logkit.jar

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}

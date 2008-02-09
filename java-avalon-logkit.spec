# NOTE
# - does not compile with java 1.6 due:
#   LogKit-1.2/src/java/org/apache/log/output/db/DefaultDataSource.java:69:
#   org.apache.log.output.db.DefaultDataSource is not abstract and does not
#   override abstract method isWrapperFor(java.lang.Class) in java.sql.Wrapper
# - http://java.sun.com/javase/6/docs/api/java/sql/Wrapper.html
%include	/usr/lib/rpm/macros.java
Summary:	Java logging toolkit
Summary(pl.UTF-8):	Biblioteka do logowania w Javie
Name:		avalon-logkit
Version:	1.2
Release:	1
Epoch:		0
License:	Apache
Group:		Development/Languages/Java
Source0:	http://www.apache.org/dist/avalon/logkit/LogKit-%{version}-src.tar.gz
# Source0-md5:	17ede0a7d297ad610b47c476757c2b96
Patch0:		%{name}-build.patch
Patch1:		%{name}-javadoc.patch
URL:		http://avalon.apache.org/logkit/
BuildRequires:	ant
#BuildRequires:	avalon-framework >= 4.1.4
BuildRequires:	javamail
BuildRequires:	jdbc-stdext
BuildRequires:	jms
BuildRequires:	jpackage-utils >= 0:1.5
BuildRequires:	junit
BuildRequires:	logging-log4j
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	servlet
BuildRequires:	jdk < 1.6
%if %(locale -a | grep -q '^en_US$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
#Requires:	avalon-framework >= 4.1.4
Requires:	jdbc-stdext
Requires:	jms
Requires:	servlet
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

%description javadoc
Javadoc for Avalon LogKit.

%description javadoc -l pl.UTF-8
Dokumentacja Javadoc do pakietu Avalon LogKit.

%prep
%setup -q -n LogKit-%{version}
%patch0 -p0
%patch1 -p1

%build
required_jars="log4j mailapi jms servlet jdbc-stdext avalon-framework junit"
PWD=$(pwd)
export CLASSPATH=$(build-classpath $required_jars):$PWD/build/classes

export LC_ALL=en_US # source code not US-ASCII
%ant clean jar javadocs

%install
rm -rf $RPM_BUILD_ROOT
# jars
install -d $RPM_BUILD_ROOT%{_javadir}
cp -a build/lib/logkit.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a build/javadocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%doc KEYS LICENSE
%{_javadir}/*.jar

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}

%include	/usr/lib/rpm/macros.java
Summary:	Java logging toolkit
Name:		avalon-logkit
Version:	1.2
Release:	0.1
Epoch:		0
License:	Apache Software License
Group:		Development/Languages/Java
URL:		http://avalon.apache.org/logkit/
Source0:	http://www.apache.org/dist/avalon/logkit/LogKit-%{version}-src.tar.gz
# Source0-md5:	17ede0a7d297ad610b47c476757c2b96
Patch0:		%{name}-build.patch
Patch1:		%{name}-javadoc.patch
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

%package javadoc
Summary:	Javadoc for %{name}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Javadoc for %{name}.

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
install build/lib/logkit.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} ${jar/-%{version}/}; done)

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

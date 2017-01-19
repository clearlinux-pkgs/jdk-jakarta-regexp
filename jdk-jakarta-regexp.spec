Name     : jdk-jakarta-regexp
Version  : 1.5
Release  : 2
URL      : http://archive.apache.org/dist/jakarta/regexp/jakarta-regexp-1.5.tar.gz
Source0  : http://archive.apache.org/dist/jakarta/regexp/jakarta-regexp-1.5.tar.gz
Summary  : No detailed summary available
Group    : Development/Tools
License  : Apache-2.0
BuildRequires : apache-ant
BuildRequires : apache-maven
BuildRequires : javapackages-tools
BuildRequires : lxml
BuildRequires : openjdk-dev
BuildRequires : python3
BuildRequires : six
BuildRequires : xmvn
Patch1: 0001-Remove-timestamp-in-javadoc.patch
Patch2: jakarta-regexp-attach-osgi-manifest.patch

%description
Ant is a build system that was developed for the Jakarta Tomcat project and
was used internally at Sun. It was originally developed by James Davidson
<duncan@eng.sun.com> and has been extended by others including myself. When
Jakarta was released as Open Source, the developer community also obtained
the source to Ant as well. This is a great addition to the community.

%prep
%setup -q -n jakarta-regexp-1.5
%patch1 -p1
#%patch2 -p1

find . -name "*.jar" -exec rm -f {} \;
cat > pom.xml << EOF
<project>
<modelVersion>4.0.0</modelVersion>
<groupId>jakarta-regexp</groupId>
<artifactId>jakarta-regexp</artifactId>
<version>1.5</version>
</project>
EOF
python3 /usr/share/java-utils/mvn_file.py : regexp
python3 /usr/share/java-utils/mvn_alias.py jakarta-regexp:jakarta-regexp regexp:regexp

%build
mkdir lib
JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk ant -Djakarta-site2.dir=. jar javadocs
python3 /usr/share/java-utils/mvn_artifact.py pom.xml build/*.jar

%install
xmvn-install  -R .xmvn-reactor -n regexp -d %{buildroot}

%files
%defattr(-,root,root,-)
/usr/share/java/regexp.jar
/usr/share/maven-metadata/regexp.xml
/usr/share/maven-poms/regexp.pom
